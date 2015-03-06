#coding=utf-8
import pexpect
import re
import tempfile
import time
import threading

'''
#新增需求，每个接口模块的类型也需要显示
self.dict format {'ge-0/0/1':{'rx':'-2','tx':'-4'},'ge-0/0/2':{'rx':'-3','tx':'-3.5'}}
'''

class H3cLightDetector(threading.Thread):
	
	def __init__(self,ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = ip
		self.spawn = spawn
		self.dict = {}
		self.interface_order = []
		self.module_type_order = []
	
	def run(self):
		self.spawn.sendline('display transceiver diagnosis interface')
		self.spawn.sendline(' '*100)
		self.spawn.sendline('display transceiver interface')
		self.spawn.sendline(' '*100)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('transceiver diagnostic',line)
				if m1:
					#暂时过滤掉40G口子
					forty_port = re.search('FortyGigE',line)
					if forty_port:
						pass						
					else:
						interface = re.findall(r'[TF].*[0-9]\/[0-9]\/[0-9][0-9]*',line)
						if interface != []:
							interface = interface[0]
							nextline = tfile.next()
							absent_key = re.search('The transceiver is absent',nextline)
							if not absent_key:
								self.interface_order.append(interface)
								m2 = re.search('Current',nextline)
								m3 = re.search('The transceiver does not support this function',nextline)
								if m2:
									x = tfile.next()
									x = tfile.next()
									newa = re.findall(r'[0-9].*',x)[0]
									newa = re.split(r'\s+',newa)
									self.dict[interface] = {'rx':newa[3],'tx':newa[4]}
								elif m3:
									self.dict[interface] = {'info':'模块不兼容，无法显示收发数值'}

				module_type = re.search('Transceiver Type',line)
				if module_type:
					print '----------------------------------',re.findall(r'[14]0G.*[A-Z]',line)
					module_type = re.findall(r'[14]0G.*[A-Z]',line)
					if module_type != []:
						module_type = module_type[0]				
					self.module_type_order.append(module_type)
			print len(self.interface_order)
			print len(self.module_type_order)		
			for index in xrange(len(self.interface_order)):
				self.dict[self.interface_order[index]]['mt'] = self.module_type_order[index]
			self.dict['interface'] = self.interface_order

		finally:
			tfile.close()
			self.spawn.close()



class JuniperLightDetector(threading.Thread):
	
	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.dict = {}
		self.interface_order = []
		self.module_type_order = []

	def run(self):
		self.spawn.sendline('show interfaces diagnostics optics| \
			match "interface|Receiver|Laser output power|Laser rx power|Optical"|no-more')
		self.spawn.sendline(' '*40)
		self.spawn.sendline('show chassis hardware | no-more')
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				interface_keycharacter = re.search('Physical interface',line)
        			if interface_keycharacter:
        				interface = re.findall(r'[a-z][a-z]-[0-9]\/[0-9]\/[0-9]*',line)[0]
        				self.interface_order.append(interface)
              				tx_line = tfile.next()
                			tx_data = re.findall(r'mW.*',tx_line)
                			if tx_data != []:
                				tx_data = tx_data[0]
                				tx_list = re.split(r'\s',tx_data)
                				rx_line = tfile.next()      		
             					rx_data = re.findall(r'mW.*',rx_line)[0]
                				rx_list = re.split(r'\s',rx_data)
                				#接口还需要增加一个key模块的型号
						self.dict[interface] = {'rx':rx_list[2],'tx':tx_list[2]}
					else:
						self.dict[interface] = {'info':'Optical diagnostics:N/A'}
			
				module_type = re.findall(r'[A-Z]FP[-+].*[0-9A-Z]',line)
				if module_type != []:
					module_type = module_type[0]
					self.module_type_order.append(module_type)

			for index in xrange(len(self.interface_order)):
				self.dict[self.interface_order[index]]['mt'] = self.module_type_order[index]
			
			self.dict['interface'] = self.interface_order


		finally:
			tfile.close()
			self.spawn.close()



                			

class HuaweiLightDetector(threading.Thread):

	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.dict = {}
		self.interface_order = []
		self.module_type_order = []

	def run(self):
		self.spawn.sendline('dis interface transceiver verbose')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('dis interface transceiver | inc "Transceiver Type"')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				key_character_1 = re.search('transceiver information:',line)
				if key_character_1:
					
					interface_name = re.findall(r'[0-9]*[A-Z]{2}[0-9]\/[0-9]\/[0-9]*',line)[0]
					self.dict[interface_name] = {}
					self.interface_order.append(interface_name)
				#抓取端口收光数据
				key_character_2 = re.search('Current RX Power',line)
				if key_character_2:	
					rx_line = re.findall(r'Current RX Power.*',line)[0]		
					rx_list = re.split(r'\s+',rx_line)
					rx_data = rx_list[4]
					rx_data = list(rx_data)
					rx_data = rx_data[1:]
					rx_data = ''.join(rx_data)
					self.dict[interface_name]['rx'] = rx_data	
				key_character_3 = re.search('Current TX Power',line)
				#抓取端口发光数据
				if key_character_3:
					tx_line = re.findall(r'Current TX Power.*',line)[0]		
					tx_list = re.split(r'\s+',tx_line)
					tx_data = tx_list[4]
					tx_data = list(tx_data)
					tx_data = tx_data[1:]
					tx_data = ''.join(tx_data)
					self.dict[interface_name]['tx'] = tx_data
				module_type = re.search('Transceiver Type',line)
				if module_type:
					module_type = re.findall(r'[0-9].*R',line)
					if module_type != []:
						module_type = module_type[0]
						self.module_type_order.append(module_type)

			for index in xrange(len(self.interface_order)):
				self.dict[self.interface_order[index]]['mt'] = self.module_type_order[index]
			self.dict['interface'] = self.interface_order

		finally:
			tfile.close()
			self.spawn.close()
			

