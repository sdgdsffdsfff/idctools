#coding=utf-8
from collections import OrderedDict
def create_cpu_mem_table(enginelist):
	
	temporary_list = []
	table_list = []
	
	for i in enginelist:
		
		temporary_list = ['<tr><td>',i.ip,'</td>','<td>',i.result["sysname"],'</td><td>',i.result['resource']["cpu"],'</td></td><td>',i.result['resource']["mem"],'</td></tr>'] 
		table_list.extend(temporary_list)
	return ''.join(table_list)




def creat_module_count(dict,list):
	type_number = []
	for i in list:
		type_number.append(str(len(dict[i])-1))	
	colors = ["info","success"]
	table_list = []
	temporary_list = []

	for i in xrange(len(list)):
		#interface = dict[list[i]]['module_type']
		tlist = dict[list[i]].keys()
		tlist.remove('sysname')
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		if int(type_number[i]) > 1:
			temporary_list = ['<tr class=',color,'><td rowspan="',type_number[i],'">',list[i],'</td><td rowspan="',\
				type_number[i],'">',dict[list[i]]['sysname'],'</td><td>',tlist[0],'</td><td>',\
				str(dict[list[i]][tlist[0]]),'</td></tr>']

			table_list.extend(temporary_list)
			tlist = tlist[1:]
			
			for j in tlist:
					temporary_list = ['<tr class=',color,'><td>',j,'</td><td>',\
					str(dict[list[i]][j]),'</td></tr>']
					table_list.extend(temporary_list)			
		else:
			temporary_list = ['<tr class=',color,'><td>',list[i],'</td><td>',dict[list[i]]['sysname'],'<td>',tlist[0],\
				'</td><td>',str(dict[list[i]][tlist[0]]),'</td></tr>']
		
			table_list.extend(temporary_list)
	return ''.join(table_list)




def create_int_err_table(dict,list):
	interface_number = []
	for i in list:
		interface_number.append(str(len(dict[i])-2))	
	colors = ["info","success"]
	table_list = []
	temporary_list = []
	for i in xrange(len(list)):
		interface = dict[list[i]]['interface']
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		if int(interface_number[i]) > 1:
			if len(dict[list[i]][interface[0]].keys()) == 3:
				temporary_list = ['<tr class=',color,'><td rowspan="',interface_number[i],'">',list[i],'</td><td rowspan="',\
						interface_number[i],'">',dict[list[i]]['sysname'],'</td><td>',interface[0],'</td><td>',\
						str(dict[list[i]][interface[0]]['in_error']),'</td><td>',\
						str(dict[list[i]][interface[0]]['out_error']),'</td></tr>']

			elif len(dict[list[i]][interface[0]].keys()) == 2:
				temporary_list = ['<tr class=',color,'><td rowspan="',interface_number[i],'">',list[i],'</td><td rowspan="',\
						interface_number[i],'">',dict[list[i]]['sysname'],'</td><td>',interface[0],'</td><td>',\
						str(dict[list[i]][interface[0]]['in_error']),'</td><td>',\
						str(dict[list[i]][interface[0]]['out_error']),'</td></tr>']
			table_list.extend(temporary_list)
			interface = interface[1:]
			for j in interface:
				if len(dict[list[i]][j].keys()) == 3:
					temporary_list = ['<tr class=',color,'><td>',j,'</td><td>',\
					str(dict[list[i]][j]['in_error']),'</td><td>',str(dict[list[i]][j]['out_error']),'</td></tr>']
						
				elif len(dict[list[i]][j].keys()) == 2:
					temporary_list = ['<tr class=',color,'><td>',j,'</td><td>',\
					str(dict[list[i]][j]['in_error']),'</td><td>',str(dict[list[i]][j]['out_error']),'</td></tr>']
				table_list.extend(temporary_list)			
		else:
			temporary_list = ['<tr class=',color,'><td>',list[i],'</td><td>',dict[list[i]]['sysname'],'<td>',interface[0],\
				'</td><td>',str(dict[list[i]][interface[0]]['in_error']),'</td><td>', \
						str(dict[list[i]][interface[0]]['out_error']),'</td></tr>']
		
			table_list.extend(temporary_list)
	return ''.join(table_list)



def create_guangshuai_table(dict,list):
	"""
	return table of guangshuai_result 
	"""
	interface_number = []
	for i in list:
		interface_number.append(str(len(dict[i])-2))	
	colors = ["info","success"]
	table_list = []
	temporary_list = []
	for i in xrange(len(list)):
		interface = dict[list[i]]['interface']
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		if int(interface_number[i]) > 1:
			if len(dict[list[i]][interface[0]].keys()) == 3:
				temporary_list = ['<tr class=',color,'><td rowspan="',interface_number[i],'">',list[i],'</td><td rowspan="',\
						interface_number[i],'">',dict[list[i]]['sysname'],'</td><td>',interface[0],'</td><td>',\
						dict[list[i]][interface[0]]['mt'],'</td><td>',str(dict[list[i]][interface[0]]['rx']),'</td><td>',\
						str(dict[list[i]][interface[0]]['tx']),'</td></tr>']

			elif len(dict[list[i]][interface[0]].keys()) == 2:
				temporary_list = ['<tr class=',color,'><td rowspan="',interface_number[i],'">',list[i],'</td><td rowspan="'\
						,interface_number[i],'">',dict[list[i]]['sysname'],'</td><td>',interface[0],\
						'</td><td colspan="3" align="right">',str(dict[list[i]][interface[0]]['info']),'</td></tr>']
			table_list.extend(temporary_list)
			interface = interface[1:]
			for j in interface:
				if len(dict[list[i]][j].keys()) == 3:
					temporary_list = ['<tr class=',color,'><td>',j,'</td><td>',dict[list[i]][j]['mt'],'</td><td>',\
					str(dict[list[i]][j]['rx']),'</td><td>',str(dict[list[i]][j]['tx']),'</td></tr>']
						
				elif len(dict[list[i]][j].keys()) == 2:
					temporary_list = ['<tr class=',color,'><td>',j,'</td>','<td colspan="3" align="right">',\
					str(dict[list[i]][j]['info']),'</td></tr>']
				table_list.extend(temporary_list)			
		else:
			if len(dict[list[i]][interface[0]].keys()) == 3:
				temporary_list = ['<tr class=',color,'><td>',list[i],'</td><td>',dict[list[i]]['sysname'],'<td>',interface[0],\
				'</td><td>',dict[list[i]][interface[0]]['mt'],'</td><td>',str(dict[list[i]][interface[0]]['rx']),'</td><td>', \
						str(dict[list[i]][interface[0]]['tx']),'</td></tr>']
			elif len(dict[list[i]][interface[0]].keys()) == 2:
				temporary_list = ['<tr class=',color,'><td>',list[i],'</td><td>',dict[list[i]]['sysname'],'<td>',interface[0],\
					'</td><td colspan="3" align="right">',str(dict[list[i]][interface[0]]['info']),'</td></tr>']
			table_list.extend(temporary_list)
	return ''.join(table_list)

def create_false_table(dict,list):
	"""
	return the  a list of ips(fail to telnet) 
	"""
	ip_list = list
        table_list = []
        for ip in ip_list:
                temporary_list = ['<tr><td>',ip,'</td><td>',dict[ip],'</td></tr>']
                table_list.extend(temporary_list)
        return ''.join(table_list)

def create_module_number_table(dict,list):
	"""
	teturn a table of the module_number
	"""
	table_list = []
	for ip in list:
		temporary_list = ['<tr><td>',ip,'</td>','<td>',dict[ip]['sysname'],'</td>','<td>',str(dict[ip]['module_number']),'</td></tr>']
		table_list.extend(temporary_list)
	return ''.join(table_list)

def create_port_channel_table_back(dict,list):
	"""
	return a table of port_channel
	"""
	table = ''
	colors = ["info","success"]
	table_list = []
	temporary_list = []
	for ip in list:
		color_index = list.index(ip)
		if color_index % 2 == 0:
			color = colors[0]
		else:
			color = colors[1]
		#ae_list = [i for i  in dict[ip].keys() if i != 'sysname']
		ae_list = dict[ip]['ae_order']
		sum_of_ae = len(ae_list)
		sum_of_interface = 0
		for ae in ae_list:
			sum_of_interface += len(dict[ip][ae]['interface'].keys())
			#the arg sum_of_interface is used to creat html table,so it should add 
			#the number that the aggregation's interface is 0
			if len(dict[ip][ae]['interface'].keys()) == 0:
				sum_of_interface += 1
		temporary_list = ['<tr class=',color,'><td rowspan="',str(sum_of_interface),'">',ip,'</td><td rowspan="',\
				str(sum_of_interface),'">',dict[ip]['sysname'],'</td>']
		table_list.extend(temporary_list)

		if len(ae_list) > 1:
			interface_list = dict[ip][ae_list[0]]['interface'].keys()
			temporary_list = ['<td rowspan="',str(len(interface_list)),'">',ae_list[0],'</td><td rowspan="',\
					str(len(interface_list)),'">',dict[ip][ae_list[0]]['state'],'</td><td rowspan="',\
					str(len(interface_list)),'">',dict[ip][ae_list[0]]['speed'],'</td>']
			table_list.extend(temporary_list)
		
			if len(interface_list) == 1:
				temporary_list = ['<td>',interface_list[0],'</td><td>',dict[ip][ae_list[0]]['interface'][interface_list[0]],\
						'</td></tr>']	
			elif len(interface_list) == 0:
				temporary_list = ['<td colspan="2" align="right">','该聚合组没有成员端口','</td></tr>']
			else:
                        	temporary_list = ['<td>',interface_list[0],'</td><td>',dict[ip][ae_list[0]]['interface'][interface_list[0]],\
                        			'</td></tr>']
				for interface  in interface_list[1:]:
					sub_list = ['<tr class=',color,'><td>',interface,'</td><td>',\
							dict[ip][ae_list[0]]['interface'][interface],'</td></tr>' ]
					temporary_list.extend(sub_list)
			table_list.extend(temporary_list)
		
			for ae in ae_list[1:]:
				interface_list = dict[ip][ae]['interface'].keys()
				temporary_list = ['<tr class=',color,'><td rowspan="',str(len(interface_list)),\
						'">',ae,'</td><td rowspan="',str(len(interface_list)),\
						'">',dict[ip][ae]['state'],'</td><td rowspan="',str(len(interface_list)),\
						'">',dict[ip][ae]['speed'],'</td>']
				table_list.extend(temporary_list)
				if len(interface_list) == 1:
					temporary_list = ['<td>',interface_list[0],'</td><td>',\
					dict[ip][ae]['interface'][interface_list[0]],'</td></tr>']	
				
				#situation that agg has no interface members
				elif len(interface_list) == 0:
					temporary_list = ['<td colspan="2" align="right">','该聚合组没有成员端口','</td></tr>']
				else:
					temporary_list = ['<td>',interface_list[0],'</td><td>',dict[ip][ae]['interface'][interface_list[0]],\
							'</td></tr>']

					for interface  in interface_list[1:]:
						sub_list = ['<tr class=',color,'><td>',interface,'</td><td>',\
							dict[ip][ae]['interface'][interface],'</td></tr>']	
						temporary_list.extend(sub_list)
				table_list.extend(temporary_list)					
			
		elif len(ae_list) == 1:
			interface_list = dict[ip][ae_list[0]]['interface'].keys()
			temporary_list = ['<td rowspan="',str(len(interface_list)),'">',ae,'</td><td rowspan="',str(len(interface_list)),\
						'">',dict[ip][ae]['state'],'</td><td rowspan="',str(len(interface_list)),\
						'">',dict[ip][ae]['speed'],'</td>']
			table_list.extend(temporary_list)
			if len(interface_list) == 1:
				temporary_list = ['<td>',interface_list[0],'</td><td>',dict[ip][ae_list[0]]['interface'][interface_list[0]],\
						'</td></tr>']

			elif len(interface_list) == 0:
				temporary_list = ['<td colspan="2" align="right">','该聚合组没有成员端口','</td></tr>']
			
			else:
				temporary_list = ['<td>',interface_list[0],'</td><td>',dict[ip][ae]['interface'][interface_list[0]],\
							'</td></tr>']
				for interface  in interface_list[1:]:
					sub_list = ['<tr class=',color,'><td>',interface,'</td><td>',dict[ip][ae]['interface'][interface],\
						'</td></tr>']
					temporary_list.extend(sub_list)

			table_list.extend(temporary_list)
	return ''.join(table_list)
         

def create_ae_table(successengine):
	table_list = []
	temporary_list = []
	colors = ["info","success"]
	for i in xrange(len(successengine)):
		ae_dict = successengine[i].result["port_channel"]
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		ae_interfaces = successengine[i].result["port_channel"].keys()
		ae_num = len(ae_interfaces)
		
		if ae_num > 1:
			temporary_list = ['<tr class=',color,'><td rowspan="',str(ae_num),'">',successengine[i].ip,'</td><td rowspan="',\
				str(ae_num),'">',successengine[i].result["sysname"],'</td><td>',ae_interfaces[0],'</td><td>',\
				ae_dict[ae_interfaces[0]]['state'],'</td><td>',ae_dict[ae_interfaces[0]]['speed'],'</td></tr>']	
			table_list.extend(temporary_list)
			ae_interfaces = ae_interfaces[1:]
			for j in ae_interfaces:
				temporary_list = ['<tr class=',color,'><td>',j,'</td><td>',ae_dict[j]['state'],'</td><td>',\
				ae_dict[j]['speed'],'</td></tr>']
				table_list.extend(temporary_list)

		elif ae_num == 1:
			temporary_list = ['<tr class=',color,'><td>',successengine[i].ip,'</td><td>',successengine[i].result["sysname"],'<td>',ae_interfaces[0],\
			'</td><td>',ae_dict[ae_interfaces[0]]['state'],'</td><td>',ae_dict[ae_interfaces[0]]['speed'],'</td></tr>']
			table_list.extend(temporary_list)
		elif ae_num == 0:
			#thereis a situation that check a lot of switchs,
			#and choose check port_channel,but maybe some switchs
			#doesn't have ae.
			temporary_list = ['<tr class=',color,'><td>',successengine[i].ip,'</td><td>',successengine[i].result["sysname"],'<td>',"Have no ae",\
			'</td><td>',"Have no ae",'</td><td>',"Have no ae",'</td></tr>']
			table_list.extend(temporary_list)

	return ''.join(table_list)






















def create_ping_table(mlist):
	"""
	return a table of ping_result
	"""
	temporary_list = []
	table_list = []
	for ip in mlist:
		div_id = mlist.index(ip) + 1
		tr_id = "t" + str(div_id)
		div_id = "h" + str(div_id)
	
		temporary_list = ['<tr id=',tr_id ,'><td class="col-sm-2"><h4>',ip,'</h4></td>','<td><h4 id=',div_id,'></h4></td></tr>']
		table_list.extend(temporary_list)
	return ''.join(table_list)


#------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	pass
