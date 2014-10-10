#from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.creattable import *
from guangshuai_test.light_decay_test import *
from guangshuai_test.detect_device import *
import time
import mako

# Create your views here.
def index(requst):
	return render_to_response('index.html')
################################################################################################################
##test the guangshuai of every switches
def guangshuai_result(request):
	#get the information
	ip_pool = request.POST.get("ips").encode("utf-8")
	username = request.POST.get("username").encode("utf-8")
	password = request.POST.get("password").encode("utf-8")
	#do some detail with the ip of the switches
	ip_list = re.split(r'\s+',ip_pool)
	#detect devices
	device_info = {}
	spawns = {} 
	#session_flag include 'success' 'timeout' 'unkonown host' 'wrong password'
	session_flag = {}
	detectors = []
	#use ip_list_counter to skip the kongge from textarea
	ip_list_counter = [i for i in ip_list if i !=""]
	for ip in ip_list_counter:
		d = distinguish_device(ip,username,password)
		detectors.append(d)
	for i in detectors:
		i.start()
	for i in detectors:
		i.join()
	
	for i in range(len(ip_list_counter)):
		device_info[ip_list_counter[i]],spawns[ip_list_counter[i]],session_flag[ip_list_counter[i]] = detectors[i].device_info,detectors[i].myspawn,detectors[i].session_flag
	#identify the ip telnet successfully whit the false	
	success_ip = [ip for ip in ip_list_counter if session_flag[ip] == "success"]
	false_ip = [ip for ip in ip_list_counter if session_flag[ip] != "success"]

	if len(success_ip): 
		#create threading objects
		collectors = []
		for i in success_ip:
			if device_info[i] == 'h3c':
	                	c = H3cLightDetector(i,username,password,spawns[i])
			elif device_info[i] == 'juniper':
				c = JuniperLightDetector(i,username,password,spawns[i])
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
			if i.dict != {}:
				dict[i.host_ip] = i.dict
		success_table = create_guangshuai_table(dict)
		
	#######################################################################
	if  len(false_ip):
		false_dict = {}
		for ip in false_ip:
			false_dict[ip] = session_flag[ip]
		false_table = create_false_table(false_dict)
		print false_table
	#######################################################################
	if len(success_ip) and len(false_ip):
		return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table,"false_table":false_table})
	elif not len(success_ip):
	#	return render_to_response("guangshuai_result.html",{'false_table':false_table})	
		for d in detectors:
	#		d.myspawn.close()
			print d.myspawn
		return render_to_response("guangshuai_result.html",{"false_table":false_table})		 
	elif not len(false_ip):
		return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table})
	else:
		return render_to_response("index.html")
	
		

def test(request):
	#return render_to_response("mytest.html",{'false_table':s})
	while True:
		print '1'
		pass
	return render_to_response("mytest.html")	
	

