import re
#oid = {
#	"h3c":{
#	"interface":"1.3.6.1.2.1.31.1.1.1.1",
#	"rx":".1.3.6.1.4.1.25506.2.70.1.1.1.9",
#	"tx":".1.3.6.1.4.1.25506.2.70.1.1.1.10",
#	"in_err":"1.3.6.1.2.1.2.2.1.14",
#	"out_err":"1.3.6.1.2.1.2.2.1.20"
#	},
#	"juniper":{
#	"interface":"1.3.6.1.2.1.31.1.1.1.1",
#	"rx":"",
#	"tx":"",
#	"in_err":"",
#	"out_err":""
#	},
#	"huawei":{
#	"interface":"",
#	"rx":"",
#	"tx":"",
#	"in_err":"",
#	"out_err":""
#	}
#
#}

sys_name = re.compile(r'".*"')


h3c_v5_flag = re.compile(r'H3C.*Version 5')
h3c_v7_flag = re.compile(r'H3C.*Version 7')
h3c_flag = re.compile(r'H3C')
h3c_int = re.compile(r'')
h3c_cpu = re.compile(r'(?P<index>[0-9]{1,3}%) in last 5 minutes')
h3c_mem = re.compile(r'Used Rate: (?P<index>[0-9]{1,2})')
h3c_relation = re.compile(r'\.(?P<index>[0-9]{1,3}) = [A-Z].*: (?P<interface>.*)')


#-----------------------------------------------------------------------------
juniper_flag = re.compile(r'Juniper')
juniper_int = re.compile(r'Physical interface: (?P<interface>xe-[0-9]/[0-9]/[0-9])')
juniper_rx = re.compile(r'Receiver signal average optical power     : .* / (?P<rx>-*.*[0-9])')
juniper_tx = re.compile(r'Laser output power                        : .* / (?P<tx>-*.*[0-9])')
juniper_cpu = re.compile(r'Idle                      (?P<cpu>[0-9]{1,2}) percent')
juniper_mem = re.compile(r'Memory utilization          (?P<mem>[0-9]{1,3}) percent')
juniper_mod = re.compile(r'[XS]FP[+-]{1,2}10G-[ELSZ]R')
juniper_ae_name = re.compile(r'Physical interface: (?P<interface>.*), Enabled')
juniper_ae_state = re.compile(r'Enabled, Physical link is (?P<state>[A-Z][a-z]{1,3})')
juniper_ae_speed = re.compile(r'Speed: (?P<speed>.*), BPDU Error:')


#----------------------------------------------------------------------------
huawei_flag = re.compile(r'HUAWEI')
flag_list = [h3c_v5_flag,h3c_v7_flag,huawei_flag,juniper_flag]