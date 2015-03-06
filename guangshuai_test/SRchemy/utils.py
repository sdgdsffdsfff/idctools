#coding=utf-8
from functools import wraps
from exception import DeviceDetectError,GetSysNameError
from .h3cengine import H3cEngine
from .juniperengine import JuniperEngine
from .huaweiengine import HuaweiEngine
from .compiledre import *
import os

def system_detector(aclass):
	"""
	This function is to recognize the types of the devices,user has two way 
	to input snmp community,first,input the snmp information in the html.
	second,use a table of database which inited before(use the script 
	offered).Additionally,users have to use snmp to recognize device.
	there is no other way supported.
	"""
	@wraps(aclass)
	def wrapper(*args,**kargs):
		try:
			ip = kargs.get("ip")
			snmp_key =kargs.get("snmp_key")
			s = snmp_walk(ip,snmp_key,"1.3.6.1.2.1.1.1.0")
			index = re_search(s,flag_list)
			if index is None:
				raise DeviceDetectError
			else:
				#get system name
				s = snmp_walk(ip,snmp_key,"1.3.6.1.2.1.1.5.0")
				pattern = sys_name.search(s)
				try:
					sysname = pattern.group(0)
					kargs["sysname"] = sysname
				except GetSysNameError:
					return aclass(ip)
		except DeviceDetectError:
			#failed to detect device return instance of FakeEngine
			return aclass(ip)
		else:
			if index == 0:
				kargs['device_flag'] = "h3c.v5"
				return H3cEngine(*args,**kargs)
			elif index ==1 :
				kargs['device_flag'] = "h3c.v7"
				return H3cEngine(*args,**kargs)
			elif index == 2:
				kargs['device_flag'] = "huawei"
				return HuaweiEngine(*args,**kargs)
			elif index == 3:
				kargs['device_flag'] = "juniper"
				return JuniperEngine(*args,**kargs)

	return wrapper



def timer(func):
	"""
	log the thime that the function cost
	"""
	@wrpas(func)
	def wrapper(*args,**kargs):
		pass
		return func(*args,**kargs)
	return wrapper

def attr_auto_set(d):
	"""
	Init a class' parameters 
	"""
	self = d.pop('self')
	for n,v in d.iteritems():
		setattr(self,n,v)

def re_search(s,re_list):
	for compiled_re in re_list:
		bol = compiled_re.search(s)
		#return first matched index
		if bol:
			return re_list.index(compiled_re)
	return None


def snmp_walk(ip,snmp_key,oid):
	"""
	Run snmpwalk command and return result 
	"""	
	command = ["snmpwalk"," -c ",snmp_key," -v"," 2c ",ip,
						" ",oid," -t"," 4"," -r"," 1"]
	command = ''.join(command)
	s = os.popen(command)
	s = s.read()
	return s 


@system_detector
class FakeEngine(object):
	"""
	This is a false class,the object will be return in
	the decorators,Please see details in @system_detector
	"""
	def __init__(self,ip):
		self.ip = ip
		self.device_flag = "snmpkey wrong or snmpwalk timeout"





