#from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.backend.creattable  import *
from guangshuai_test.backend.light_decay_test  import *
from guangshuai_test.backend.detect_device import *
from guangshuai_test.backend.module_number_counter import *
from guangshuai_test.backend.aggregation_detector import *
import time
#import mako

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
	sysname = {}
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
		device_info[ip_list_counter[i]],spawns[ip_list_counter[i]],session_flag[ip_list_counter[i]],sysname[ip_list_counter[i]] = \
			detectors[i].device_info,detectors[i].myspawn,detectors[i].session_flag,detectors[i].sysname
	#identify the ip telnet successfully whit the false	
	success_ip = [ip for ip in ip_list_counter if session_flag[ip] == "success"]
	false_ip = [ip for ip in ip_list_counter if session_flag[ip] != "success"]

	if len(success_ip): 
		#create threading objects
		collectors = []
		for i in success_ip:
			if device_info[i] == 'h3c':
				c = H3cLightDetector(i,username,password,spawns[i])
			elif device_info[i] == 'huawei':
				c = HuaweiLightDetector(i,username,password,spawns[i])
			collectors.append(c)

     	#run the threading objects
		for i in range(len(collectors)):
			collectors[i].start()
			print collectors[i],'-----------------------------start'
        #wait for the all the threading finished
		for i in range(len(collectors)):
			collectors[i].join()
			print collectors[i],'------------------------------stop'
        #merge the dicts and return to views.py of django
		success_dict = {}
		ip_for_create_table = []
		for i in collectors:
			if i.dict != {}:
				i.dict['sysname'] = sysname[i.host_ip]
				success_dict[i.host_ip] = i.dict
				ip_for_create_table.append(i.host_ip)
		if success_dict != {}:
			success_table = create_guangshuai_table(success_dict,ip_for_create_table)
		
	#######################################################################
	if  len(false_ip):
		false_dict = {}
		for ip in false_ip:
			false_dict[ip] = session_flag[ip]
		false_table = create_false_table(false_dict,false_ip)
	#######################################################################
	if len(success_ip) and len(false_ip) and success_dict != {}:
		return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table,"false_table":false_table})
	elif not len(success_ip):
		return render_to_response("guangshuai_result.html",{"false_table":false_table})		 
	elif not len(false_ip) and success_dict != {}:
		return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table})
	elif success_dict == {}:
		return render_to_response("index.html")


#############################################################################################################################################################
#############################################################################################################################################################
def module_number(request):
	ip_pool = request.POST.get("ips").encode("utf-8")
 	username = request.POST.get("username").encode("utf-8")
 	password = request.POST.get("password").encode("utf-8")
 	ip_list = re.split(r'\s+',ip_pool)
 	device_info = {}
 	spawns = {}
 	session_flag = {}
 	detectors = []
	sysname = {}
	ip_list_counter = [i for i in ip_list if i !=""]
	for ip in ip_list_counter:
		d = distinguish_device(ip,username,password)
		detectors.append(d)
	for i in detectors:
		i.start()
	for i in detectors:
		i.join()	

	for i in range(len(ip_list_counter)):
		device_info[ip_list_counter[i]],spawns[ip_list_counter[i]],session_flag[ip_list_counter[i]],sysname[ip_list_counter[i]] = \
			detectors[i].device_info,detectors[i].myspawn,detectors[i].session_flag,detectors[i].sysname
        #identify the ip telnet successfully whit the false     
	success_ip = [ip for ip in ip_list_counter if session_flag[ip] == "success"]
	false_ip = [ip for ip in ip_list_counter if session_flag[ip] != "success"]
	
	if len(success_ip):
		#create threading objects
		collectors = []
		for i in success_ip:
			if device_info[i] == 'h3c':
				c = H3cModuleNumberCounter(i,username,password,spawns[i])
			elif device_info[i] == 'juniper':
				c = JuniperModuleNumberCounter(i,username,password,spawns[i])
			collectors.append(c)
		for i in range(len(collectors)):
			collectors[i].start()
			print collectors[i],'-----------------------------start'
        #wait for the all the threading finished
        for i in range(len(collectors)):
            collectors[i].join()
            print collectors[i],'------------------------------stop'
        success_dict = {}
        ip_for_create_table = []
        summary_number = 0
        for i in collectors:
			tem_dict = {}
			tem_dict['sysname'] = sysname[i.host_ip]
			tem_dict['module_number'] = i.number
			success_dict[i.host_ip] = tem_dict
			ip_for_create_table.append(i.host_ip)
			summary_number += i.number
			if success_dict != {}:
				module_number_table = create_module_number_table(success_dict,ip_for_create_table)
        info = ' 成功登录到'+str(len(success_ip))+' 台交换机，探测到光模块总数为：'+ str(summary_number)

        #######################################################################
        if  len(false_ip):
                false_dict = {}
                for ip in false_ip:
                        false_dict[ip] = session_flag[ip]
                false_table = create_false_table(false_dict,false_ip)
        #######################################################################
        if len(success_ip) and len(false_ip) and success_dict != {}:
                return render_to_response("module_number.html",{"module_number_table":module_number_table,"false_table":false_table,'info':info})
        elif not len(success_ip):
                return render_to_response("module_number.html",{"false_table":false_table})
        elif not len(false_ip) and success_dict != {}:
                return render_to_response("module_number.html",{"module_number_table":module_number_table,'info':info})
        else:
                return render_to_response("index.html")



######################################################################################################################################################
#####################################################################################################################################################
####################################################################################################################################################
def port_channel(request):
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
	sysname = {}
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
		device_info[ip_list_counter[i]],spawns[ip_list_counter[i]],session_flag[ip_list_counter[i]],sysname[ip_list_counter[i]] = \
			detectors[i].device_info,detectors[i].myspawn,detectors[i].session_flag,detectors[i].sysname
	#identify the ip telnet successfully whit the false	
	success_ip = [ip for ip in ip_list_counter if session_flag[ip] == "success"]
	false_ip = [ip for ip in ip_list_counter if session_flag[ip] != "success"]

	if len(success_ip): 
		#create threading objects
		collectors = []
		for i in success_ip:
			if device_info[i] == 'h3c':
				c = H3cAggregationDetector(i,username,password,spawns[i])
			elif device_info[i] == 'juniper':
				c = JuniperAggregationDetector(i,username,password,spawns[i])
			collectors.append(c)

     		   #run the threading objects
		for i in range(len(collectors)):
			collectors[i].start()
			print collectors[i],'-----------------------------start'
        #wait for the all the threading finished
		for i in range(len(collectors)):
			collectors[i].join()
			print collectors[i],'------------------------------stop'
        #merge the dicts and return to views.py of django
		success_dict = {}
		ip_for_create_table = []
		for i in collectors:
			if i.dict != {}:
				i.dict['sysname'] = sysname[i.host_ip]
				success_dict[i.host_ip] = i.dict
				ip_for_create_table.append(i.host_ip)
		#print 'ip_for_create_table:',ip_for_create_table
		if success_dict != {}:
			#print '----------------------------------------------------------------success_table',success_dict
			port_channel_table = create_port_channel_table(success_dict,ip_for_create_table)

		
		
	#######################################################################
	if  len(false_ip):
		false_dict = {}
		for ip in false_ip:
			false_dict[ip] = session_flag[ip]
		false_table = create_false_table(false_dict,false_ip)
	#######################################################################
	if len(success_ip) and len(false_ip) and success_dict != {}:
		return render_to_response("port_channel.html",{"port_channel_table":port_channel_table,"false_table":false_table})
	elif not len(success_ip):
		return render_to_response("port_channel.html",{"false_table":false_table})		 
	elif not len(false_ip) and success_dict != {}:
		return render_to_response("port_channel.html",{"port_channel_table":port_channel_table})
	elif success_dict == {}:
		return render_to_response("index.html")
	
##############################################################################################################################################
############################################################################################################################################
###########################################################################################################################################



























def test(request):
    return render_to_response("mytest.html")	
	

