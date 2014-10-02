#from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.creattable import *
from guangshuai_test.light_decay_test import *
from guangshuai_test.detect_device import *
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
	print "ip_list",ip_list
	#detect devices
	device_info = {}
	spawns = {}
	success_flag = {}
	for ip in ip_list:
		if ip != "":
			print "ip:",ip
			device_info[ip],spawns[ip],success_flag[ip] =  distinguish_device(ip,username,password)	
		

	#identify the ip telnet successfully whit the false	
	success_ip = []
	false_ip = []
	for ip in ip_list:
		if ip != "":
			if success_flag[ip] == True:
				success_ip.append(ip)
			else:
				false_ip.append(ip)
	

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
			dict[i.host_ip] = i.dict
		table = create_table(dict)
	#######################################################################3
	if not len(false_ip):
		pass
	

	#############################3
	return render_to_response("guangshuai_result.html",{"guangshuai_table":table})


def test(request):
	return render_to_response("mytest.html")
	

