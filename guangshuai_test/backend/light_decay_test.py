#!/usr/bin/python
#coding=utf-8
import threading
import sys
import tempfile
import re 
import readline
import Queue
import pexpect

'''
self.dict format {'ge-0/0/1':{'rx':'-2','tx':'-4'},'ge-0/0/2':{'rx':'-3','tx':'-3.5'}}
'''


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

	def __init__(self,host_ip,username,password,spawn):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.username = username
		self.password = password
		self.spawn = spawn
		self.dict = {}

	def run(self):
		self.spawn.sendline('dis interface transceiver verbose')
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
		finally:
			tfile.close()
			self.spawn.close()

