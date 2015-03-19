#coding=utf-8
import subprocess
import re


def ping_large_packet(host,packet_number,packet_size,data_dict):

	command = ["ping","-c",packet_number,host,"-s",packet_size,"-i","0.2","-W","3"]

			 ## ["ping","-c","10","10.182.0.14","-s","20","-i","1","-W","3"]
	print command
	p = subprocess.Popen(command,stdout=subprocess.PIPE)
	data_dict[host] = "timeout"
	busy = True
	ping_result = p.stdout.readline()
	while busy:
		ping_result = p.stdout.readline()
		
		#print '##################',ping_result,'----------------------------'
		if ping_result != "":
			last_line = re.search(r'packets transmitted',ping_result)
			time = re.findall(r'time=.*s',ping_result)
			if time != []:
				data_dict[host] = ping_result
			elif last_line:
				data_dict[host] = ping_result
			
		else:
			ping_result = p.stdout.readline()
			if ping_result == "":
				busy = False
			else:
				continue


