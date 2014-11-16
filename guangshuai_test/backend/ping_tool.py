#!/usr/bin/python
#coding=utf-8
import subprocess
import re
import redis
from guangshuai_test.backend.idctools_config import *

#在这里将ping的结果插入到redis数据库

def ping_large_packet(host,packet_number,packet_size):
	busy = True
	command = ["ping","-c",packet_number,host,"-s",packet_size,"-i","1","-W","3"]
	p = subprocess.Popen(command,stdout=subprocess.PIPE)
	redis_connection.set(host,"timeout")
	while busy:
		ping_result = p.stdout.readline()
		if ping_result != "":
			last_line = re.search(r'packets transmitted',ping_result)
			time = re.findall(r'time=.*s',ping_result)
			if time != []:
				redis_connection.set(host,ping_result)
			elif last_line:
				redis_connection.set(host,ping_result)
		else:
			busy = False
