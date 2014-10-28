#!/usr/bin/python
#coding=utf-8
import threading
import tempfile
import re
import pexpect

class H3cAggregationDetector(threading.Thread):
	def __init__(self,host_ip,username,password,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.username = username
		self.password = password
		self.spawn = spawn
		self.dict = {}


	def run(self):
		self.spawn.sendline('dis interface Bridge-Aggregation')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('dis link-aggregation verbose')
		self.spawn.sendline(' '*50)
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
					print '-------------------------------',a
					x = tfile.next()
					x = tfile.next()
					x = tfile.next()
					m2 = re.search('speed mode',x)
					print '----------------------------------------------------------------!',x
					if m2:
						#list2 = re.split(r'\s+',x)
						
						speed = re.findall(r'[a-zA-Z0-9]*-[a-z]{5}',x)
						#print speed[0]
						self.dict[a[0]] = {}
						self.dict[a[0]]['state'] = a[3]
						#self.dict[a[0]]['speed'] = list2[1]
						self.dict[a[0]]['speed'] = speed[0]
						

				m2 = re.search('Aggregation Interface',line)
				if m2:
					list3 = re.findall(r'Aggregation Interface.*',line)[0]
					list3 = re.split(r'\s+',list3)
					
					for subline in tfile:
						m3 = re.search('Oper-Key',subline)
						if m3:
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
			
		finally:
			tfile.close()
			self.spawn.close()




class JuniperAggregationDetector(threading.Thread):
	pass




class HuaweiAggregationDetector(threading.Thread):
	pass
