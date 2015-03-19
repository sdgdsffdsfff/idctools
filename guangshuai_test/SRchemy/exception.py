"""
User defined global  exception and warning classes.
"""
class DeviceDetectError(Exception):
	"""
	Define the error that recognize device failed
	"""
	pass

class ConnectError(Exception):
	"""
	Define the error that connect to the device failed
	"""
	pass

class ExecuteError(Exception):
	"""Define the error discovery while execute a command"""
	pass


class GetSysNameError(Exception):
	pass

class ExecuteActionError(Exception):
	pass 



 