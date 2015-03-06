from .baseengine import BaseEngine


class HuaweiEngine(BaseEngine):
	"""
	Handle with huawei's device 
	"""
	def __init__(self,username,password,connect_protocal=None,
		device_flag=None,action=None,ip=None,sysname=None):
		super(HuaweiEngine,self).__init__(username,password,
			connect_protocal=connect_protocal,device_flag=device_flag,
			action=action,ip=ip,sysname=sysname)


	def _init_work(self):
		pass
