

def get_input(username,password,snmpkey,ippool):
	ip_pool = request.POST.get("ips").encode("utf-8")
	username = request.POST.get("username").encode("utf-8")
	password = request.POST.get("password").encode("utf-8")
	snmpkey = request.POST.get("snmpkey")
	return ip_pool,username,password,snmpkey
