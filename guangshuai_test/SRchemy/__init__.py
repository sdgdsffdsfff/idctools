#from .baseengine import BaseEngine
from utils import FakeEngine
import threading



def connect(ip_list,username,password,snmp,action):
	"""
	Due to the ip_list generate a list of object of defferent engine's 
	instance,and return the list
	example:
		ip_list = ["10.168.0.34",
					"10.168.0.35",
					"10.168.0.36",
					"10.168.0.37",
					"10.168.0.38",
					"10.168.0.39"]
		snmp = "snmp commuity"
		con = gen_connect(ip_list,snmp)
	action relationship
	0   ----  show_dacy
	1   ----  show_in_out_error
	2   ----  show_module
	3
	4

	"""
	#this list is to store the instances of engine
	ins_list = []
	th_list = []

	def gen_engine(ip,username,password,snmp,action):
		en = FakeEngine(username,password,ip=ip,action=action,snmp_key=snmp)
		ins_list.append(en)
	
	for ip in ip_list:
		con = threading.Thread(target=gen_engine,args=(ip,username,password,snmp,action))
		con.start()
		th_list.append(con)
	for con in th_list:
		con.join()
	return ins_list





