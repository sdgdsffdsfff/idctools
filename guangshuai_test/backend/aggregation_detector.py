#!/usr/bin/python
#coding=utf-8
import threading
import tempfile
import re
import pexpect
'''

self.dict format 

'''
class H3cAggregationDetector(threading.Thread):

	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.dict = {}
		self.ae_order = []

	def run(self):
		self.spawn.sendline(' '*3)
		self.spawn.sendline('dis interface Bridge-Aggregation')
        	self.spawn.sendline(' '*100)
       		self.spawn.sendline('dis link-aggregation verbose')
        	self.spawn.sendline(' '*100)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)

			for line in tfile:	
				m1 = re.search('current state',line)
				if m1:

					a = re.findall(r'Bridge-Agg.*',line)[0]
					a = re.split(r'\s+',a)
					self.ae_order.append(a[0])
					self.dict[a[0]] = {}
					x = tfile.next()
					x = tfile.next()
					x = tfile.next()
					m2 = re.search('speed mode',x)
					if m2:
						speed = re.findall(r'[a-zA-Z0-9]*-[a-z]{5}',x)
						self.dict[a[0]]['state'] = a[3]
						self.dict[a[0]]['speed'] = speed[0]							
				m2 = re.search('Aggregation Interface',line)
				m3 = re.search('Aggregate Interface',line)
				if m2 or m3:
					list3 = re.findall(r'Aggregat.* Interface.*',line)[0]
					list3 = re.split(r'\s+',list3)						
					for subline in tfile:
						m3 = re.search('Oper-Key',subline)
						m4 = re.search('Port',subline)
						if m3 and m4:
							self.dict[list3[2]]['interface'] = {}
							x = tfile.next()
							
							while True:
								x = tfile.next()
								m3 = re.search('GE',x)
								if m3:
									list4 = re.findall(r'[A-Z]*[A-Z][A-Z][0-9]\/[0-9]\/[0-9][0-9]*.*',x)[0]
									list4 = re.split(r'\s+',list4)									
									self.dict[list3[2]]['interface'][list4[0]] = list4[1]
								else:
									break
							break
			self.dict['ae_order'] = self.ae_order		
			
			
		finally:
			tfile.close()
			self.spawn.close()





class JuniperAggregationDetector(threading.Thread):
	pass




class HuaweiAggregationDetector(threading.Thread):

	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.dict = {}
		self.ae_order = []

	def run(self):
		self.spawn.sendline('dis int eth')
                self.spawn.sendline(' '*50)
                self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				ae_key = re.search(r'Eth-Trunk',line)
       				if ae_key:
              				eth_interface = re.findall(r'Eth-Trunk[0-9]*',line)[0]
                			eth_state = re.findall(r'[UD][A-Z]*[PN]',line)
                			self.dict[eth_interface] = {}
                			self.ae_order.append(eth_interface)
                			self.dict[eth_interface]['state'] = eth_state[0]
                			self.dict[eth_interface]['interface'] = {}
               				next_line = tfile.next()
                			next_line = tfile.next()
                			next_line = tfile.next()
                			bw_key = re.findall(r'Current .*bps',next_line)

                			if bw_key != []:

                				bw_key = re.split(r'\s+',bw_key[0])
                				
                      				self.dict[eth_interface]['speed'] = bw_key[2]
                			else:
                        			self.dict[eth_interface]['speed'] = '0Gbps'

       			 	port_key =re.search(r'PortName',line)
       	 			if port_key:
                			line = tfile.next()
                			line = tfile.next()
                			while True:
                        			interface = re.findall(r'[0-9]*GE[0-9]\/[0-9]\/[0-9]*',line)
                        			if interface != []:
                                			interface = interface[0]
                                			interface_state = re.findall(r'[UD][A-Z]*[NP]',line)[0]
                                			self.dict[eth_interface]['interface'][interface] = interface_state
                                			line = tfile.next()
                        			else:
                                			break
                        self.dict['ae_order'] = self.ae_order
                finally:
			tfile.close()
			self.spawn.close()
			print self.dict
			
	
