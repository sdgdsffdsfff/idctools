#!/usr/bin/python
#coding=utf-8
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
		self.spawn.sendline(' '*50)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('transceiver diagnostic',line)
				if m1:
					a = re.findall(r'[A-Z]*[a-z]*[a-z]*-*[A-Z][a-z]{6}[A-Z][a-z]{7}[0-9]\/[0-9]\/[0-9][0-9]*',line)[0]
					interface =  a
					nextline = tfile.next()
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
		finally:
			tfile.close()
			self.spawn.close()



class JuniperLightDetector(threading.Thread):
	pass


class HuaweiLightDetector(threading.Thread):
	pass


