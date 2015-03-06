from ..SRchemy import *


#snmp = "123321cisco123456"
##snmp = "cisco12312312312snaj"
#ip_list = [
#"10.193.0.20"
#]


snmp = "123321cisco123456"
ip_list = ["10.193.2.27"]

x =  connect(ip_list,"lijie-it","1.cqmyg2.ysdss.",snmp,[1])



for i in x:
	i.start()


for i in x:
	i.join()

for i in x:
	print i.ip,"------------------------",i.result


