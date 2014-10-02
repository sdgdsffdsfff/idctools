#!/usr/bin/python
import pexpect
import re
import tempfile

def distinguish_device(ip,username,password):
	#this function include the process of err login failed... 
	success_flag = True
	myspawn = pexpect.spawn('telnet '+ ip)
	index = myspawn.expect(["login:", "Username:","(?i)Unknown host", pexpect.EOF, pexpect.TIMEOUT])
	
	if index == 0:
		device_info = "juniper"
		myspawn.sendline(username)
		myspawn.expect("Password:")
		myspawn.sendline(password)
	elif index == 1:
		myspawn.sendline(username)
		myspawn.expect("Password:")
		myspawn.sendline(password)
		myspawn.sendline('n')
		index2 = myspawn.expect([" % Incomplete command*","syntax error*"])
		if index2 == 0:
			device_info = "h3c"
		elif index2 == 1:
			device_info = "juniper"
	
	elif index == 2 or index == 3:
		success_flag = False	

	
	return device_info,myspawn,success_flag
