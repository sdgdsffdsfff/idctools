#from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.creattable import *
from guangshuai_test.transerver_module import *
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
	
	#create threading objects
	collectors = []
        for i in ip_list:
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
	table = create_table(dict)
	return render_to_response("guangshuai_result.html",{"guangshuai_table":table})




