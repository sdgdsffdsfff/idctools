#!/usr/bin/python
import getpass
import sys
import telnetlib
import time
import tempfile
import re 
import readline
import threading 
import Queue

#define three queue to count the numbers of sw and modules
'''
sw_queue = Queue.Queue()
mod_queue = Queue.Queue()
telnet_success = Queue.Queue()
telnet_success = Queue.Queue()
'''
class Collector(threading.Thread):
	
	def __init__(self,sw_ip,username,password):
		threading.Thread.__init__(self)
		self.sw_ip = sw_ip
		self.username = username
		self.password = password
		self.dict = {}
	
	def run(self):
#create telnet session to switch sw_ip
###########################################################################################
		try:
			tn = telnetlib.Telnet(self.sw_ip,23,5)
		except:
		#	print "%10s"%self.sw_ip,"%90s"%"telnet failed"
			return
		tn.read_until("Username:")
		tn.write(self.username + "\n")
		if self.password:
			tn.read_until("Password:")
			tn.write(self.password + "\n")
##############################################################################################
#execute the commands
#############################################################################################
		tn.write("display transceiver diagnosis interface\n")
		tn.write("quit\n")	
############################################################################################
#create temporary file 
		try:
			log = tempfile.TemporaryFile()
			log.write(tn.read_until('finish'))
			log.seek(0)
	#		print "%10s"%self.sw_ip
			while True:
				line = log.readline()
				m1 = re.search('transceiver diagnostic',line)
				if line:
					if m1:
						list = re.split(r'\s+',line)
						interface =  list[0]
						nextline = log.readline()
						m2 = re.search('Current',nextline)
					#	m3 = re.search('The transceiver does not support this function',nextline)
						if m2:
							x = log.readline()
							x = log.readline()
							newlist = re.split(r'\s+',x)
						        self.dict[interface] = {'rx':newlist[4],'tx':newlist[5]}
					#	elif m3:
						#	print "%30s"%'     |-----------------------',"%30s"%interface,"%51s"%'The transceiver does not support this function'
						else:continue
					else:continue
				else:
					break
		finally:
			log.close()		



'''
if __name__ == "__main__":
	#print the title
	
	#create threading objects
	for i in host:
		c = Collector(i,username,password)
		collectors.append(c)
	
	#run the threading objects
	for i in range(len(collectors)):
		collectors[i].start()

	#wait for the all the threading finished
	for i in range(len(collectors)):
		collectors[i].join()
	
	#merge the dicts and return to views.py of django
	dict = {}
	for i in collectors:
		dict[i.sw_ip] = i.dict

	print dict
'''





		





	
	

	
