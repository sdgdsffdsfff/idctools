import threading
import pexpect
from .exception import ConnectError,ExecuteActionError
from functools import wraps
from .compiledre import *
import re,os
from collections import OrderedDict

class BaseEngine(threading.Thread):
	"""
	The Base class for all device processor's class
	"""
	def __init__(self,username,password,connect_protocal=None,
		device_flag=None,action=None,ip=None,sysname=None,snmp_key=None):
		super(BaseEngine,self).__init__()
		self.username = username
		self.password = password
		self.ip = ip
		#action is a list include number transmited from views
		#
		#whether login in the switch or not 
		self.logined = False
		self.action  = action
		#flag define the session weather connect successfully or failed
		self.session_flag = "failed"
		#flag to log the device's type
		self.device_flag = device_flag
		self.sysname = sysname
		self.snmp_key = snmp_key
		#result is a dict and store all the information collected from the 
		#device
		self.result = OrderedDict()
		self.result["deacy"] = OrderedDict()
		self.result["sysname"] = self.sysname
		self.result["interface_error"] = OrderedDict()
		self.result["resource"] = {}
		self.result["module_type"] = {}
		self.result["port_channel"] = OrderedDict()
		self.connect_protocal = connect_protocal
		self.interface_name = {}


	def choose_oid(self):
		"""
		Due to different device choose different oids
		"""
		pass

	def connect(self,cprotocol = "telnet"):
		"""
		Use different protocal to connect due to the parameter cprotocol,if 
		user has nottranmit a spcified connect_protocol,'telnet will be 
		default'
		"""
		pass
		
	def close_connection(self):
		"""Close the commection"""
		if self.session_flag == 'connected':
			self.spawn.close()

	def run(self):
		if 1 in self.action:
			self.show_deacy()
		if 2 in self.action:
			self.show_in_out_error()
		if 3 in self.action:
			self.show_sys_resource()
		if 4 in self.action:
			self.count_module_type()
		if 5 in self.action:
			self.show_sn()
		if 6 in self.action:
			self.show_err_log()
		if 7 in self.action:
			self.show_port_channel()
		
		#self.show_in_out_error()
		#try:
		#	for action in self.action_list:
		#		action
		#except ExecuteActionError("Error in BaseEngine's run function"):
		#	pass
		#finally:
		#	self.close()
		self.close_connection()

	def check_interface_index(self):
		"""
		This function check whether  interface_name is empty dict,if so,run 
		this function to get the self.interface_name
		"""
		if len(self.interface_name.keys()) == 0:
			interface_name = self._snmp_walk("1.3.6.1.2.1.31.1.1.1.1")
			self.interface_name = self._oid_string_to_dict(interface_name)
		else:
			pass

	def execute(self):
		"""
		Try to execute commands on the switches or routers.and this
		function will generate a instance of class Transaction
		"""
		raise NotImplementedError

	def show_port_channel(self):
		"""
		"""
		raise NotImplementedError


	def show_deacy(self):
		"""
		show deacy
		"""
		self.check_interface_index()
		#interface_name = self._snmp_walk("1.3.6.1.2.1.31.1.1.1.1")
		deacy_tx_info = self._snmp_walk(".1.3.6.1.4.1.25506.2.70.1.1.1.9")
		deacy_rx_info = self._snmp_walk(".1.3.6.1.4.1.25506.2.70.1.1.1.12")
		module_type = self._snmp_walk(".1.3.6.1.4.1.25506.2.70.1.1.1.2")
		#get the interface name and index relationships
		#self.interface_name = self._oid_string_to_dict(interface_name)
		deacy_tx_info = self._oid_string_to_dict(deacy_tx_info)
		deacy_rx_info = self._oid_string_to_dict(deacy_rx_info)
		module_type = self._oid_string_to_dict(module_type)
		for index in deacy_tx_info.keys():
			tx = int(deacy_tx_info[index])/100.0
			rx = int(deacy_rx_info[index])/100.0
			if tx != 0:
				self.result["deacy"][self.interface_name[index]] = {}
				self.result["deacy"][self.interface_name[index]]['rx'] = rx
				self.result["deacy"][self.interface_name[index]]['tx'] = tx
				self.result["deacy"][self.interface_name[index]]['mt'] = \
															module_type[index]
		self.result["deacy"]["interface"] = self.result["deacy"].keys()
		

	def show_in_out_error(self):
		self.check_interface_index()
		in_error = self._snmp_walk("1.3.6.1.2.1.2.2.1.14")
		out_error = self._snmp_walk("1.3.6.1.2.1.2.2.1.20")
		in_error = self._oid_string_to_dict(in_error)
		out_error = self._oid_string_to_dict(out_error)
		for index in in_error.keys():
			if in_error[index] != '0' or out_error[index] != '0':
				self.result["interface_error"][self.interface_name[index]] = {}
				self.result["interface_error"][self.interface_name[index]]\
					["in_error"] = in_error[index]
				self.result["interface_error"][self.interface_name[index]]\
					["out_error"] = out_error[index] 
		self.result["interface_error"]["interface"] = self.result["interface_error"].keys()

	def show_sys_resource(self):
		"""
		Get information of cpu usage,memory usage
 		"""
		raise NotImplementedError

	def show_sn(self):
		"""
		Get serial number of device,mudole
		"""
		raise NotImplementedError

	def show_err_log(self):
		raise NotImplementedError

	def count_module_type(self):
		raise NotImplementedError
	
	
	def _snmp_walk(self,oid):
		"""
		all sub class will Inheritance this function,but they needn't use
		this function ,all the actions need snmp will write in the BaseEngine
		the result is a list
		"""
		command = ["snmpwalk"," -c ", self.snmp_key ," -v"," 2c ",self.ip,
						" ",oid," -t"," 5"," -r"," 1"]
		command = ''.join(command)
		result = os.popen(command)
		result = result.read()
		result_list = re.split(r'\n',result)
		result_list = result_list[:-1]
	 	return result_list

	def _oid_string_to_dict(self,int_list):
		"""
		deal with the int_list and return a dict
		example
		if int_list=[
		"iso.3.6.1.2.1.31.1.1.1.1.334 = STRING: "Ten-GigabitEthernet3/0/43"",
		"iso.3.6.1.2.1.31.1.1.1.1.335 = STRING: "Ten-GigabitEthernet3/0/44""
		]
		then the dict will be
		{
		"334":"Ten-GigabitEthernet3/0/43",
		"335":"Ten-GigabitEthernet3/0/44"
		}
		"""
		relation_dict = {}
		for  str in int_list:
			relation = h3c_relation.search(str)
			relation_dict[relation.group('index')] = relation.group('interface')
		return relation_dict



	def check_login(self):
		if self.logined == False:
			#login to the switch
			self.connect() 


	def count_module(self,tlist):
		"""
		example tlist = ['SFP+-10G-SR', 'SFP+-10G-SR']
		return a dict {"SFP+-10G-SR":2}
		"""
		tdict = {}
		for i in tlist:
			if i not in tdict.keys():
				tdict[i] = 1
			else:
				tdict[i] += 1

		return tdict



class Transaction(object):
	"""
	It will generate a object of Transaction if objects of Connection run
	execute function,this class it to log the executed commands and offer
	two function commit and rollback() to contral the operation
	"""

	def __init__(self):
		pass

	def commit():
		"""save the changed configuration on the device"""
		pass

	def rollback():
		"""
		Delete the new added commands on the device if something wrong during
		operate time
		"""
		pass

class Plain(object):
	pass


