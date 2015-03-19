from .baseengine import BaseEngine
from .exception import ConnectError,ExecuteActionError
import pexpect,re
from .compiledre import *

class H3cEngine(BaseEngine):
	"""
	Handle with h3c's device 
	"""
	def __init__(self,username,password,connect_protocal=None,
		action=None,ip=None,sysname=None,snmp_key=None,device_flag=None):
		
		super(H3cEngine,self).__init__(username,password,
			connect_protocal=connect_protocal,device_flag=device_flag,
			action=action,ip=ip,sysname=sysname,snmp_key=snmp_key)
		#self.snmp_key = "bjcc443kkadc89ac360"
		#print "h3c ip is ",ip

	def connect(self,cprotocol = "telnet"):
		if self.connect_protocal is not None:
			_cprotocol = self.connect_protocal
		else:
			_cprotocol = cprotocol
		try:
			if _cprotocol == "telnet":
				self.spawn = pexpect.spawn('telnet '+ self.ip,timeout=5,
					searchwindowsize=2030)
				i = self.spawn.expect(["Username:","login:"])
				if i == 0 or i == 1:
					self.spawn.sendline(self.username)
				self.spawn.expect("Password:")
				self.spawn.sendline(self.password)
				i = self.spawn.expect(["% Login failed!",">"])
				if i == 0:
					self.session_flag = "password wrong"
					self.device_flag = "password wrong"
					raise ConnectError
				else:
					self.session_flag = "connected"
			elif _cprotocol == "ssh":
				self.spawn = pexpect.spawn(
					'ssh ' + self.username + '@' + self.ip,
					timeout=5,searchwindowsize=2030)
		except ConnectError:
			#close the spawn
			self.spawn.close()
		else:
			self.session_flag = "connected"
    
	def show_sys_resource(self):
		"""
		Get information of cpu usage,memory usage
 		"""
		if(self.check_login()):
			self.spawn.sendline("dis memory")
			self.spawn.expect(">")
			mem = self.spawn.before
			mem_usage = h3c_mem.search(mem)
			self.spawn.sendline("dis cpu")
			self.spawn.expect(">")
			cpu = self.spawn.before
			cpu_usage = h3c_cpu.search(cpu)
			self.result['resource']['mem'] = mem_usage.group('index')+"%"
			self.result['resource']['cpu'] = cpu_usage.group('index')
		else:
			pass

	def count_module_type(self):
		module_type = self._snmp_walk(".1.3.6.1.4.1.25506.2.70.1.1.1.2")
		module_type = self._oid_string_to_dict(module_type)
		deacy_type = module_type.values()
		self.result['module_type'] = self.count_module(deacy_type)
		

	def show_sn(self):
		pass


	def show_port_channel(self):
		#check login
		if(self.check_login()):
			self.spawn.sendline("dis interface Bridge-Aggregation")
			self.spawn.sendline(" "*20)
			self.spawn.expect(">")
			ae_info = self.spawn.before
			ae_int = h3c_ae_name.findall(ae_info)
			ae_int_state = h3c_ae_state.findall(ae_info)
			ae_int_speed = h3c_ae_speed.findall(ae_info)
			for index in xrange(len(ae_int)):
				self.result["port_channel"][ae_int[index]] = \
					{'speed':ae_int_speed[index],'state':ae_int_state[index]}
		else:
			pass

