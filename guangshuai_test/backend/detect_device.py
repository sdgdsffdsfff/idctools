#!/usr/bin/python
#coding=utf-8
import pexpect
import re
import tempfile
import time
import threading

'''
the function of distinguish of h3c , huawei and juniper has been done
cisco and other company's swith will be added later
'''

class distinguish_device(threading.Thread):

	def __init__(self,ip,username,password,connect_protocol):
		threading.Thread.__init__(self)
		self.ip = ip
		self.username = username
		self.password = password
		self.session_flag = 'false'
		self.device_info = 'init'
		self.sysname = ''
		self.connect_protocol = connect_protocol

	def run(self):
		#login failed charecter of deferent company
		#Login incorrect   --------------------------juniper 
		#% Login failed!-----------------------------huasan
		#Error: Username or password error.----------huawei
		if self.connect_protocol == "telnet":
			self.myspawn = pexpect.spawn('telnet '+ self.ip,timeout=10)
		elif self.connect_protocol == "ssh":
			print "create ssh detector"
			self.myspawn = pexpect.spawn('ssh ' + self.username + '@' + self.ip,timeout=10)
			print  'ssh ' + self.username + '@' + self.ip
		
		first_expect = self.myspawn.expect(["login:", "Username:", \
					"(?i)Unknown host","Unknown server error",pexpect.EOF, pexpect.TIMEOUT,"yes/no","password"])
		
		
		if first_expect == 0:
			self.myspawn.sendline(self.username)
			self.myspawn.expect("Password:")
			self.myspawn.sendline(self.password)
			after_login_expect = self.myspawn.expect(['% Login failed!','>','Login incorrect'])
                        if after_login_expect == 0 or after_login_expect == 2:
                                self.session_flag = 'wrong username or password'
                                self.myspawn.close()
                        else:
                                self.session_flag = 'success'
                                self.myspawn.sendline('n')

                                send_n_h3c_or_juniper_expect = self.myspawn.expect([" % Unrecognized command found*","syntax error*"])
				#need to ensure!!!!
                                if send_n_h3c_or_juniper_expect == 0:
					h3c_hostname = self.myspawn.expect([">"])
					if h3c_hostname  == 0:
						self.device_info = "h3c"
						sysname_info =  self.myspawn.before.strip()
						sysname_infoa = re.findall(r'<.*',sysname_info)[0]
						sysname = list(sysname_infoa)
						sysname = sysname[1:]
                               			self.sysname  = ''.join(sysname)
                               			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!self.sysname',self.sysname
                                       		
				elif send_n_h3c_or_juniper_expect == 1:
					self.device_info = "juniper"
					juniper_hostname = self.myspawn.expect([">"])
					if juniper_hostname == 0:
						sysname_info =  self.myspawn.before
						sysname_infoa = re.findall(r'@.*',sysname_info)[0]
						sysname = list(sysname_infoa)
						sysname = sysname[1:]
                               			self.sysname  = ''.join(sysname)
					



		#the Character is "Username",so the device is huawei or h3c
		elif first_expect == 1:
			self.myspawn.sendline(self.username)
			self.myspawn.expect("Password:")
			self.myspawn.sendline(self.password)
			after_username_expect = self.myspawn.expect(['% Login failed!','>', \
				'Error: Username or password error.','The initial password poses'])
			#'% Login failed!','Error: Username or password error.','Login incorrect', '>','The initial password poses'
			if after_username_expect == 0 or after_username_expect == 2:
				self.session_flag = 'wrong username or password'
				self.myspawn.close()
			#there is a situation that the huawei swith cloed the waring of changing passwd,
			#ans in this situation,the character of both h3c and huawei is same 	
			elif after_username_expect == 1:
				sysname_info =  self.myspawn.before.strip()
				sysname_infoa = re.findall(r'<.*',sysname_info)[0]
				sysname = list(sysname_infoa)
                                sysname = sysname[1:]
                                self.sysname  = ''.join(sysname)
				self.session_flag = 'success'
				self.sysname  = ''.join(sysname)
				self.myspawn.sendline('n')
				
				h3c_or__huawei_hostname = self.myspawn.expect([" % Unrecognized command found *", \
					"Error: Unrecognized command found at '^' position."])
				if h3c_or__huawei_hostname == 0:
					self.device_info = "h3c"
				elif h3c_or__huawei_hostname == 1:
					self.device_info = "huawei"
			
			elif after_username_expect == 3:
                                self.session_flag = 'success'
				self.device_info = "huawei"
				self.myspawn.sendline('n')
				self.myspawn.sendline(' ')
				huawei_hostname = self.myspawn.expect([">"])
				if huawei_hostname  == 0:
					sysname_info =  self.myspawn.before.strip()
					sysname_infoa = re.findall(r'<.*',sysname_info)[0]
					sysname = list(sysname_infoa)
                              		sysname = sysname[1:]
                              		self.sysname  = ''.join(sysname)
                          
####################################################################################################################################
		elif first_expect == 2 or first_expect == 3: 
			self.session_flag = 'unknown host'
			self.myspawn.close()
		elif  first_expect == 4 or first_expect == 5:
			self.session_flag = 'timeout'	
			self.myspawn.close()
		elif first_expect == 6:
			self.myspawn.sendline('yes')
			self.myspawn.expect('password:')
			self.myspawn.sendline(self.password)

			##增加密码错误逻辑处理，输入一次密码返回再输入的时候，应该断开
			password_expect = self.myspawn.expect(["Permission denied",">"])
			if password_expect == 0:
				self.session_flag = "password wrong"
				self.myspawn.sendcontrol('c')
				self.myspawn,close()
			elif password_expect == 1:
				####
				self.myspawn.sendline('n')

				device_info_expect = self.myspawn.expect([" % Unrecognized command found*","syntax error*",\
							"The initial password poses","% Incomplete command*"])

				if device_info_expect == 0 or device_info_expect == 3:
					self.device_info = "h3c"
				   	h3c_hostname = self.myspawn.expect([">"])
					sysname_info =  self.myspawn.before.strip()
					sysname_infoa = re.findall(r'<.*',sysname_info)[0]
					sysname = list(sysname_infoa)
                               		sysname = sysname[1:]
                                	self.sysname  = ''.join(sysname)
				if device_info_expect == 1:
					self.device_info = "juniper"
					juniper_hostname = self.myspawn.expect([">"])
					if juniper_hostname == 0:
						sysname_info =  self.myspawn.before
						sysname_infoa = re.findall(r'@.*',sysname_info)[0]
						sysname = list(sysname_infoa)
						sysname = sysname[1:]
                               			self.sysname  = ''.join(sysname)

				if device_info_expect ==2:
					self.device_info = "huawei"
					huawei_hostname = self.myspawn.expect([">"])
					sysname_info =  self.myspawn.before.strip()
					sysname_infoa = re.findall(r'<.*',sysname_info)[0]
					sysname = list(sysname_infoa)
                               		sysname = sysname[1:]
                                	self.sysname  = ''.join(sysname)

		elif first_expect == 7:
			print 'expect is password,send password'
			self.myspawn.sendline(self.password)

			##增加密码错误逻辑处理，输入一次密码返回再输入的时候，应该断开
			password_expect = self.myspawn.expect(["Permission denied",">"])
			if password_expect == 0:
				self.session_flag = "password wrong"
				self.myspawn.sendcontrol('c')
				self.myspawn,close()
			elif password_expect == 1:
				####
				self.session_flag = "success"
				self.myspawn.sendline('n')
				device_info_expect = self.myspawn.expect([" % Unrecognized command found*","syntax error*",\
							"The initial password poses","% Incomplete command*"])

				if device_info_expect == 0 or device_info_expect == 3:
					self.device_info = "h3c"
					h3c_hostname = self.myspawn.expect([">"])					
					sysname_info =  self.myspawn.before.strip()
					print sysname_info
					sysname_infoa = re.findall(r'<.*',sysname_info)[0]
					sysname = list(sysname_infoa)
                               		sysname = sysname[1:]
                                	self.sysname  = ''.join(sysname)
				if device_info_expect == 1:
					self.device_info = "juniper"
					juniper_hostname = self.myspawn.expect([">"])
					if juniper_hostname == 0:
						sysname_info =  self.myspawn.before
						sysname_infoa = re.findall(r'@.*',sysname_info)[0]
						sysname = list(sysname_infoa)
						sysname = sysname[1:]
                               			self.sysname  = ''.join(sysname)

				if device_info_expect ==2:
					self.device_info = "huawei"
					huawei_hostname = self.myspawn.expect([">"])
					sysname_info =  self.myspawn.before.strip()
					sysname_infoa = re.findall(r'<.*',sysname_info)[0]
					sysname = list(sysname_infoa)
                               		sysname = sysname[1:]
                                	self.sysname  = ''.join(sysname)
                              
	#	return device_info,myspawn,session_flag
