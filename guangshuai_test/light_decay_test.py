#!/usr/bin/python
import threading
import sys
import tempfile
import re 
import readline
import Queue
import pexpect

#there is a function to identify the device and return a pexpect spawn to these classes


class H3cLightDetector(threading.Thread):
	def __init__(self,host_ip,username,password,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.username = username
		self.password = password
		self.spawn = spawn
		self.dict = {}
	
	def run(self):
		self.spawn.sendline('display transceiver diagnosis interface')
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('transceiver diagnostic',line)
				if m1:
					list = re.split(r'\s+',line)
					interface =  list[0]
					nextline = tfile.next()
					m2 = re.search('Current',nextline)
					m3 = re.search('The transceiver does not support this function',nextline)
					m4 = re.search('Error: The transceiver is absent.',nextline)
					if m2:
						x = tfile.next()
						x = tfile.next()
						newlist = re.split(r'\s+',x)
						self.dict[interface] = {'rx':newlist[4],'tx':newlist[5]}
					elif m3:
						self.dict[interface] = {'info':'模块不兼容，无法显示收发数值'}
					elif m4:
						self.dict[interface] = {'info':'接口无光模块'}
		finally:
			tfile.close()
			#print 'close spawn in h3clightconnector-----------------------------!'
			self.spawn.close()


class JuniperLightDetector(threading.Thread):
	pass


class HuaweiLightDetector(threading.Thread):
	pass


