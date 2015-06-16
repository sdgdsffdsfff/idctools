from .baseengine import BaseEngine
from .exception import ConnectError,ExecuteActionError
import pexpect,re,os
from .compiledre import *

class JuniperEngine(BaseEngine):
	"""
	Handle with juniper's device 
	"""
	def __init__(self,username,password,connect_protocal=None,
		device_flag=None,action=None,ip=None,sysname=None,snmp_key=None):
		super(JuniperEngine,self).__init__(username=username,password=password,
			connect_protocal=connect_protocal,device_flag=device_flag,
						action=action,ip=ip,sysname=sysname,snmp_key=snmp_key)


	def show_deacy(self):
		"""
		If you want to get juniper dom information,you need to login 
		int the device and send the commands
		"""
                print "11"
		if(self.check_login()):
                        self.spawn.sendline(' ')
			self.spawn.expect(juniper_cmdline)
                        print "before",self.spawn.before
                        print "send kong ge"
			self.spawn.sendline('show interfaces diagnostics optics | no-more')
			self.spawn.expect(juniper_cmdline)
			self.spawn.expect(juniper_cmdline)
			deacy_info = self.spawn.before
                        print "deacy_info",deacy_info
                        print "##"
                        print "a",deacy_info
			deacy_int = juniper_int.findall(deacy_info)
			deacy_rx = juniper_rx.findall(deacy_info)
			deacy_tx = juniper_tx.findall(deacy_info)
			self.spawn.sendline('show chassis hardware | no-more')
			self.spawn.expect(">")
			deacy_type_info = self.spawn.before
                        print deacy_type_info
			deacy_type = re.findall(r'[XS]FP[+-]{1,2}10G-[ELSZ]R',
				deacy_type_info)
			print deacy_type
                        print deacy_int
			for i in xrange(len(deacy_int)):
				self.result["deacy"][deacy_int[i]] = {}
				self.result["deacy"][deacy_int[i]]['rx'] = deacy_rx[i]
				self.result["deacy"][deacy_int[i]]['tx'] = deacy_tx[i]
				self.result["deacy"][deacy_int[i]]['mt'] = \
									deacy_type[i]
                        print "self interfaces######",self.result["deacy"].keys()
			self.result["deacy"]["interface"] = self.result["deacy"].keys()
		else:
			pass
														
	def connect(self,cprotocol="telnet"):
		if self.connect_protocal is not None:
			_cprotocol = self.connect_protocal
		else:
			_cprotocol = cprotocol
		try:
			if _cprotocol == "telnet":
				self.spawn = pexpect.spawn('telnet '+ self.ip,timeout=10,
					searchwindowsize=2030)
				self.spawn.expect("login:")
				self.spawn.sendline(self.username)
				self.spawn.expect("Password:")
				self.spawn.sendline(self.password)
				i = self.spawn.expect(["Login incorrect",juniper_cmdline])
				if i == 0:
					self.session_flag = "password wrong"
					self.device_flag = "password wrong"
					raise ConnectError
				else:
					self.session_flag = "connected"

			elif _cprotocol == "ssh":
				self.spawn = pexpect.spawn(
					'ssh ' + self.username + '@' + self.ip,
					timeout=10,searchwindowsize=2030)

		except ConnectError:
			#close the spawn
                        print "failed"
			self.spawn.close()
		else:
			self.session_flag = "connected"


			
	def show_sys_resource(self):
		"""
		Get information of cpu usage,memory usage
 		"""
 		if(self.check_login()):
 			self.spawn.sendline("show chassis routing-engine")
 			self.spawn.expect(juniper_cmdline)
 			usage = self.spawn.before
 			cpu_usage = juniper_cpu.search(usage)
 			cpu_usage = str(int(100 - int(cpu_usage.group('cpu'))))+"%"
 			self.result['resource']['cpu'] = cpu_usage
 			mem_usage = juniper_mem.search(usage)
 			self.result['resource']['mem'] = mem_usage.group('mem')+"%"
 		else:
 			pass

	def count_module_type(self):
		"""
		"""
		if(self.check_login()):
			self.spawn.sendline('show chassis hardware | no-more')
			self.spawn.expect(juniper_cmdline)
			deacy_type_info = self.spawn.before
			deacy_type = juniper_mod.findall(deacy_type_info)
			self.result['module_type'] = self.count_module(deacy_type)


	def show_port_channel(self):
		if(self.check_login()):
			self.spawn.sendline('show interface ae* | no-more')
			self.spawn.expect(juniper_cmdline)
			ae_info = self.spawn.before
			ae_int = juniper_ae_name.findall(ae_info)
			ae_int_state = juniper_ae_state.findall(ae_info)
			ae_int_speed = juniper_ae_speed.findall(ae_info)
			for index in xrange(len(ae_int)):
				self.result["port_channel"][ae_int[index]] = \
					{'speed':ae_int_speed[index],'state':ae_int_state[index]}
		else:
			pass
		



