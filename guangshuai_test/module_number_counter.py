#!/usr/bin/python
#coding=utf-8
import threading
import sys
import tempfile
import re 
import readline
import Queue
import pexpect



class H3cModuleNumberCounter(threading.Thread):
	def __init__(self,host_ip,username,password,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.username = username
		self.password = password
		self.spawn = spawn
		self.number = 0


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
					if m2 or m3:
						self.number += 1
		finally:
			tfile.close()
			self.spawn.close()
