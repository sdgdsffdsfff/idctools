#!/usr/bin/python
#coding=utf-8
import threading
import tempfile
import re
import pexpect


class H3cAggretionDetector(threading.Thread):
	def __init__(self,host_ip,username,password,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.username = username
		self.password = password
		self.spawn = spawn
		self.dict = {}


	def run(self):
		self.spawn.sendline('display interface Bridge-Aggregation')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('display link-aggregation verbose')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('quit')


		try:
			tfile = tempfile.TeporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('current state',line)
				if m1:
					list1 = re.split(r'\s+',line)
					x = tfile.next()
					x = tfile.next()
					x = tfile.next()
					m2 = re.search('speed mode',x)
					if m2:
						list2 = re.split(r'\s+',x)
						self.dict[list1[1]] = {}
						self.dict[list[1]]['state'] = list1[4]
						self.dict[list[1]]['speed'] = list2[1]
				m4 = re.search('Aggregation Interface',line)
				if m4:
					list3 = re.split(r'\s+',line)
					for subline in tfile:
						m3 = re.search('Oper-Key',subline)
						if m3:
							self.dict[list3[2]]['interface'] = {}
							x = tfile.next()
							while True:
								x = tfile.next()
								m5 = re.search('GE',x)
								if m5:
									list4 = re.split(r'\s+',x)
									self.dict[list3[2]]['interface'][list4[1]] = list4[2]
								else:
									break
							break
		finally:
			tfile.close()
			self.spawn.close()
