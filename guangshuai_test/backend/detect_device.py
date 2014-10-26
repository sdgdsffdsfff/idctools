#!/usr/bin/python
import pexpect
import re
import tempfile
import time
import threading
class distinguish_device(threading.Thread):
	def __init__(self,ip,username,password):
		threading.Thread.__init__(self)
		self.ip = ip
		self.username = username
		self.password = password
		#this function include the process of err login failed... 
		self.session_flag = 'false'
		self.device_info = 'init'
		self.sysname = ''

	def run(self):
		self.myspawn = pexpect.spawn('telnet '+ self.ip,timeout=7)
		index = self.myspawn.expect(["login:", "Username:","(?i)Unknown host","Unknown server error",pexpect.EOF, pexpect.TIMEOUT])
	
		if index == 0:
			self.myspawn.sendline(self.username)
			self.myspawn.expect("Password:")
			self.myspawn.sendline(self.password)
		elif index == 1:
			self.myspawn.sendline(self.username)
			self.myspawn.expect("Password:")
			self.myspawn.sendline(self.password)
			i = self.myspawn.expect(['% Login failed!','>'])
			if i == 0:
				self.session_flag = 'wrong username or password'
				self.myspawn.close()
			else:
				sysname_info =  self.myspawn.before.strip()
				sysname = list(sysname_info)
				sysname = sysname[1:]
				self.sysname  = ''.join(sysname)
				self.session_flag = 'success'
				self.myspawn.sendline('n')
				
				index2 = self.myspawn.expect([" % Incomplete command*","syntax error*"])
				if index2 == 0:
					self.device_info = "h3c"
	
		elif index == 2 or index == 3: 
			self.session_flag = 'unknown host'
			self.myspawn.close()
		elif  index == 5 or index == 4:
			self.session_flag = 'timeout'	
			print '1'
			self.myspawn.close()
		else:
			print 'Eoh'
	#	return device_info,myspawn,session_flag
	