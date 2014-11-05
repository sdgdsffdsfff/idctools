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
	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.number = 0

	def run(self):
		self.spawn.sendline('dis transceiver manuinfo interface')
		self.spawn.sendline(' '*100)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('transceiver manufacture',line)
				if m1:
					nextline = tfile.next()
					m2 = re.search('Serial Number',nextline)
					m3 = re.search('The transceiver does not support this function',nextline)
					if m2 or m3:
						self.number += 1
		finally:
			tfile.close()
			self.spawn.close()




class JuniperModuleNumberCounter(threading.Thread):

	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.number = 0

	def run(self):
		self.spawn.sendline('show interfaces diagnostics optics \
				 | match "Physical interface" | no-more')
		self.spawn.sendline('exit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				m1 = re.search('Physical interface',line)
				if m1:
					self.number += 1
		finally:
			tfile.close()
			self.spawn.close()





class HuaweiModuleNumberCounter(threading.Thread):

	def __init__(self,host_ip,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.spawn = spawn
		self.number = 0

	def run(self):
		print 'start run '
		self.spawn.sendline('dis interface transceiver')
		self.spawn.sendline(' '*50)
		self.spawn.sendline('quit')
		self.spawn.expect(pexpect.EOF)
		try:
			tfile = tempfile.TemporaryFile()
			tfile.write(self.spawn.before)
			tfile.seek(0)
			for line in tfile:
				key_character = re.search('transceiver information',line)
				if key_character:
					self.number += 1
		finally:
			tfile.close()
			self.spawn.close()

