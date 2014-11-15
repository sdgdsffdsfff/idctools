#!/usr/bin/python
#coding=utf-8
import subprocess
import re 
import redis

#在这个脚本中，将对redis数据库增加数据
def ping_large_packet(host,package_number,size):
	busy = True
	command = ["ping","-c",package_number,host ,"-s",size ,"-i","0.01","-W","3"]
	p = subprocess.Popen(command,stdout= subprocess.PIPE)
	while busy:
        	strpingresult = p.stdout.readline()
       		if strpingresult != "":
                	time = re.findall(r'time=.*s',strpingresult)
                	if time != []:
                        	print time[0]
        	else:
                	busy = False




