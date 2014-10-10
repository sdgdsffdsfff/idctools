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
#	ip_pool = request.GET.get("ips").encode("utf-8")
#	username = request.GET.get("username").encode("utf-8")
#	password = request.GET.get("password").encode("utf-8")
	#do some detail with the ip of the switches
	ip_list = re.split(r'\s+',ip_pool)
	#detect devices
	device_info = {}
	spawns = {}
	#session_flag include 'success' 'timeout' 'unkonown host' 'wrong password'
	session_flag = {}
	detectors = []
	ip_list_counter = []
	#use ip_list_counter to skip the kongge from textarea
	for ip in ip_list:
		if ip != "":
			ip_list_counter.append(ip)
	for ip in ip_list_counter:
		d = distinguish_device(ip,username,password)
		detectors.append(d)
		print d,time.ctime()
	for i in detectors:
		i.start()
	for i in detectors:
		i.join()
	#do some detail with the ip of the switches
	ip_list = re.split(r'\s+',ip_pool)
	#detect devices
	device_info = {}
	spawns = {}
	#session_flag include 'success' 'timeout' 'unkonown host' 'wrong password'
	session_flag = {}
	detectors = []
	ip_list_counter = []
	#use ip_list_counter to skip the kongge from textarea
	for ip in ip_list:
		if ip != "":
			ip_list_counter.append(ip)
	for ip in ip_list_counter:
		d = distinguish_device(ip,username,password)
		detectors.append(d)
		print d,time.ctime()
	for i in detectors:
		i.start()
	for i in detectors:
		i.join()
	for i in range(len(ip_list_counter)):
		device_info[ip_list_counter[i]],spawns[ip_list_counter[i]],session_flag[ip_list_counter[i]] = detectors[i].device_info,detectors[i].myspawn,detectors[i].session_flag
	print time.ctime()
	#identify the ip telnet successfully whit the false	
	success_ip = []
	false_ip = []
	for ip in ip_list_counter:
		if ip != "":
			if session_flag[ip] == 'success':
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
		print collectors
        #wait for the all the threading finished
		for i in range(len(collectors)):
			collectors[i].join()
	#	print time.ctime()
        #merge the dicts and return to views.py of django
		dict = {}
		for i in collectors:
			if i.dict != {}:
				dict[i.host_ip] = i.dict
		success_table = create_guangshuai_table(dict)
	#	print time.ctime()
		
	#######################################################################
	if  len(false_ip):
		false_dict = {}
		for ip in false_ip:
			false_dict[ip] = session_flag[ip]
		false_table = create_false_table(false_dict)
	#######################################################################
	if len(success_ip) and len(false_ip):
		print 'Time:',time.ctime(),success_table,false_table
	#	return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table,"false_table":false_table})
	elif not len(success_ip):
		print time.ctime(),false_table
		print time.ctime()
	#	return render_to_response("guangshuai_result.html",{'false_table':false_table})	
		print threading.active_count()  #return the number of the result of threading.enumerate
		print threading.enumerate() #return The list includes daemonic threads,
		print threading.current_thread()
		print len(false_table)
		return render_to_response("mytest.html",{'false_table':false_table})	
		 
	elif not len(false_ip):
		return render_to_response("guangshuai_result.html",{"guangshuai_table":success_table})
	else:
		return render_to_response("index.html")
	
		

def test(request):
	#return render_to_response("mytest.html",{'false_table':s})
	table ="<tr><td>10.10.10.38</td><td>timeout</td></tr><tr><td>10.10.10.46</td><td>timeout</td></tr><tr><td>10.10.10.47</td><td>timeout</td></tr><tr><td>10.10.10.44</td><td>timeout</td></tr><tr><td>10.10.10.45</td><td>timeout</td></tr><tr><td>10.10.10.42</td><td>timeout</td></tr><tr><td>10.10.10.43</td><td>timeout</td></tr><tr><td>10.10.10.40</td><td>timeout</td></tr><tr><td>10.10.10.41</td><td>timeout</td></tr><tr><td>10.10.10.48</td><td>timeout</td></tr><tr><td>10.10.10.49</td><td>timeout</td></tr><tr><td>10.10.10.20</td><td>timeout</td></tr><tr><td>10.10.10.21</td><td>timeout</td></tr><tr><td>10.10.10.22</td><td>timeout</td></tr><tr><td>10.10.10.23</td><td>timeout</td></tr><tr><td>10.10.10.24</td><td>timeout</td></tr><tr><td>10.10.10.25</td><td>timeout</td></tr><tr><td>10.10.10.26</td><td>timeout</td></tr><tr><td>10.10.10.27</td><td>timeout</td></tr><tr><td>10.10.10.28</td><td>timeout</td></tr><tr><td>10.10.10.29</td><td>timeout</td></tr><tr><td>10.10.10.1</td><td>timeout</td></tr><tr><td>10.10.10.33</td><td>timeout</td></tr><tr><td>10.10.10.3</td><td>timeout</td></tr><tr><td>10.10.10.2</td><td>timeout</td></tr><tr><td>10.10.10.5</td><td>timeout</td></tr><tr><td>10.10.10.4</td><td>timeout</td></tr><tr><td>10.10.10.7</td><td>timeout</td></tr><tr><td>10.10.10.6</td><td>timeout</td></tr><tr><td>10.10.10.9</td><td>timeout</td></tr><tr><td>10.10.10.8</td><td>timeout</td></tr><tr><td>10.10.10.31</td><td>timeout</td></tr><tr><td>10.10.10.50</td><td>timeout</td></tr><tr><td>10.10.10.30</td><td>timeout</td></tr><tr><td>10.10.10.36</td><td>timeout</td></tr><tr><td>10.10.10.37</td><td>timeout</td></tr><tr><td>10.10.10.32</td><td>timeout</td></tr><tr><td>10.10.10.15</td><td>timeout</td></tr><tr><td>10.10.10.14</td><td>timeout</td></tr><tr><td>10.10.10.17</td><td>timeout</td></tr><tr><td>10.10.10.16</td><td>timeout</td></tr><tr><td>10.10.10.11</td><td>timeout</td></tr><tr><td>10.10.10.10</td><td>timeout</td></tr><tr><td>10.10.10.13</td><td>timeout</td></tr><tr><td>10.10.10.12</td><td>timeout</td></tr><tr><td>10.10.10.39</td><td>timeout</td></tr><tr><td>10.10.10.34</td><td>timeout</td></tr><tr><td>10.10.10.19</td><td>timeout</td></tr><tr><td>10.10.10.18</td><td>timeout</td></tr><tr><td>10.10.10.35</td><td>timeout</td></tr>"
	print len(table)
	return render_to_response("mytest.html",{'false_table':table})	
	

