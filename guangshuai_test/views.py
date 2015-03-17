#coding=utf-8
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.utils.createtable  import *
from guangshuai_test.utils.tool  import *
from guangshuai_test.SRchemy import *
import time
import re
import json


def index(requst):
	index = 1 
	return render_to_response('index.html',{'index':index})

##test the guangshuai of every switches
def guangshuai_result(request):
	pass


def once_check(request):
	ip_pool = request.POST.get("ips").encode("utf-8")
	username = request.POST.get("username").encode("utf-8")
	password = request.POST.get("password").encode("utf-8")
	snmpkey = request.POST.get("snmpkey").encode("utf-8")
	#connect_protocol = request.POST.get("radiobutton").encode("utf-8")
	check_box_list = request.REQUEST.getlist('checkbox') 
	ip_list = re.split(r'\s+',ip_pool)
	ip_list = [i for i in ip_list if i !=""]
	action = []
	for i in check_box_list:
		action.append(int(i))
	print action
	result_list  =  connect(ip_list,username,password,snmpkey,action)
	guangshuai_table,module_number_table,int_err_table,cpu_mem_table = \
    											None,None,None,None
	ae_table = None
	order_list = []
	for i in result_list:
		order_list.insert(ip_list.index(i.ip),i)
	
	false_ip = []
	false_dict = {}

	for i in result_list:
		if i.device_flag == "snmpkey wrong or snmpwalk timeout":
			false_ip.append(i.ip)
			false_dict[i.ip] = "snmpkey wrong or snmpwalk timeout"
		else:
			i.start()
	for i in result_list:
		if i.device_flag == "snmpkey wrong or snmpwalk timeout":
			pass
		else:
			i.join()
	for i in result_list:
		if i.device_flag == "password wrong":
			false_ip.append(i.ip)
			false_dict[i.ip] = "password wrong"

	success_list = []
	
	for i in order_list:
		if i.ip not in false_ip:
			success_list.append(i)

	if 1 in action:
		#self.show_deacy()
		guangshuai_dict = {}
		for i in success_list:
			if  i.result["deacy"] != {}:
				guangshuai_dict[i.ip] = i.result["deacy"]

		ip_for_create_table = []
		for i in success_list:
			if i.result["deacy"]["interface"] != []:
				guangshuai_dict[i.ip] = i.result["deacy"]
				guangshuai_dict[i.ip]["sysname"] =  i.result['sysname']
				ip_for_create_table.append(i.ip)

		if guangshuai_dict != {}:
			guangshuai_table = create_guangshuai_table(guangshuai_dict,
			ip_for_create_table)
	
	if 2 in action:
		#self.show_in_out_error()
		int_err_dict = {}
		for i in success_list:
			if  i.result["interface_error"] != {}:
				int_err_dict[i.ip] = i.result["interface_error"]

		ip_for_create_table = []
		for i in success_list:
			if i.result["interface_error"]["interface"] != []:
				int_err_dict[i.ip] = i.result["interface_error"]
				int_err_dict[i.ip]["sysname"] =  i.result['sysname']
				ip_for_create_table.append(i.ip)

		if int_err_dict != {}:
			int_err_table = create_int_err_table(int_err_dict,
												ip_for_create_table)
	if 3 in action:
		cpu_mem_table = create_cpu_mem_table(success_list)
	if 4 in action:
		type_dict = {}
		ip_for_create_table = []
		for i in success_list:
			if i.result["module_type"] != {}:
				type_dict[i.ip] = i.result["module_type"]
				type_dict[i.ip]["sysname"] =  i.result['sysname']
				ip_for_create_table.append(i.ip)
		

		sum_dict = {}
		for i in success_list:
			t_list = i.result["module_type"].keys()
			t_list.remove('sysname')
			for j in xrange(len(t_list)):
				if t_list[j] in sum_dict.keys():
					sum_dict[t_list[j]] += \
						int(i.result["module_type"][t_list[j]])
				else:
					sum_dict[t_list[j]] = \
						int(i.result["module_type"][t_list[j]])



		#print '~~~~~~~~~~~~~~~~~~~~~~~~',sum_dict

 		module_number_table = creat_module_count(type_dict,ip_for_create_table)
	if 5 in action:
		#self.show_sn()
		pass
	if 6 in action:
		#self.show_err_log()
		pass

	if 7 in action:
		ae_table = create_ae_table(success_list)



	false_table = create_false_table(false_dict,false_ip)
	success_ip = []
	return render_to_response("guangshuai_result.html",
		{"guangshuai_table":guangshuai_table,
		"false_table":false_table,
		"int_err_table":int_err_table,
		"cpu_mem_table":cpu_mem_table,
		"module_number_table":module_number_table,
		"ae_table":ae_table})






def module_number(request):
	pass

def port_channel(request):
	pass

def ping_threading(request):
	#传递这个参数到data_ajax中
	global ping_ip_list_counter

	ip_pool = request.POST.get("ips").encode("utf-8")
	packet_size = request.POST.get("packet_size").encode("utf-8")
	packet_number = request.POST.get("packet_number").encode("utf-8")
	ip_list = re.split(r'\s+',ip_pool)
	ping_ip_list_counter = [i for i in ip_list if i !=""]
	ping_collectors = []

	for ip in ping_ip_list_counter:
		sub_ping = threading.Thread(target=ping_large_packet,
							args=(ip,packet_number,packet_size))
		ping_collectors.append(sub_ping)
	for sub_ping_instance in ping_collectors:
		sub_ping_instance.start()

	table = create_ping_table(ping_ip_list_counter)
	return render_to_response("ping_result.html",{'ping_table':table})

def test(request):
	return render_to_response("mytest.html")	
	
def test2(request):
	#check = request.POST.get("gs").encode("utf-8")
	check_box_list = request.REQUEST.getlist('check_box') 
		


	return render_to_response("mytest2.html")





def data_ajax(request):	
	#接受用户传递过来的参数，在redis数据库中查询结果并返回
	sub_ip_pool = ping_ip_list_counter
	response_data = []
	sub_dict = {}
	sub_dict["info"] = len(sub_ip_pool)
	#第一个info用来存储列表的长度
	response_data.append(sub_dict)
	for index in xrange(len(sub_ip_pool)):
		temp_dict = {}
		temp_dict["info"] = redis_connection.get(sub_ip_pool[index])
		response_data.append(temp_dict)
	return HttpResponse(json.dumps(response_data),
							content_type="application/json")