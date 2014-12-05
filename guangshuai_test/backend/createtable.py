#!/usr/bin/python
#coding=utf-8

#提升合并字符串的效率

#def merge_string(list):
#	return ''.join(list)

def create_guangshuai_table(dict,list):
	
        #switch_list = dict.keys()
	#the function will eventually return the string opject table to the html
	#count numbers of every switch
	interface_number = []
	for i in list:
		interface_number.append(str(len(dict[i])-2))	
	colors = ["info","success"]
	table_list = []
	temporary_list = []
		
	#create table with forloop

	for i in xrange(len(list)):
		print dict[list[i]]
		interface = dict[list[i]]['interface']
		#interface = [ j for j in dict[list[i]].keys() if j != 'sysname']
		#define the color 
		
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		#identify how many numbers does the switch has
		#if interface_number >1 ,merge the row 

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
				#print '------------------------------j',j,len(dict[list[i]][j].keys())
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

	print table_list
	return ''.join(table_list)

#######################################################################################################################################
#######################################################################################################################################
def create_false_table(dict,list):
#	ip_list = dict.keys()
	ip_list = list
        table_list = []
        for ip in ip_list:
                temporary_list = ['<tr><td>',ip,'</td><td>',dict[ip],'</td></tr>']
                table_list.extend(temporary_list)
                print 'extend----------------------'
        return ''.join(table_list)


def create_module_number_table(dict,list):
	table_list = []
	for ip in list:
		temporary_list = ['<tr><td>',ip,'</td>','<td>',dict[ip]['sysname'],'</td>','<td>',str(dict[ip]['module_number']),'</td></tr>']
		table_list.extend(temporary_list)
	return ''.join(table_list)




############################################################################################################################################
############################################################################################################################################
def create_port_channel_table(dict,list):
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
			print interface_list
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
					print interface
					sub_list = ['<tr class=',color,'><td>',interface,'</td><td>',dict[ip][ae]['interface'][interface],\
						'</td></tr>']
					temporary_list.extend(sub_list)

			table_list.extend(temporary_list)
	return ''.join(table_list)


            
def create_ping_table(mlist):
	temporary_list = []
	table_list = []
	for ip in mlist:
		div_id = mlist.index(ip) + 1
		tr_id = "t" + str(div_id)
		div_id = "h" + str(div_id)
	
		temporary_list = ['<tr id=',tr_id ,'><td class="col-sm-2"><h4>',ip,'</h4></td>','<td><h4 id=',div_id,'></h4></td></tr>']
		table_list.extend(temporary_list)
	return ''.join(table_list)



###############################################################################################################################
###############################################################################################################################
if __name__ == "__main__":
	dict = {'1.1.1.1':{'ge0':{'info':'not support'},'ge1':{'rx':1,'tx':5},'ge2':{'rx':1,'tx':3}},'2.2.2.2':{'ge3':{'rx':4,'tx':5},'ge1':{'rx':1,'tx':2}},'3.3.3.3':{'tge3':{'rx':-1,'tx':-2.5},'Tge2':{'rx':0.1,'tx':2},'tge1':{'rx':1,'tx':2},'tge0':{'rx':1,'tx':2}},'4.4.4.4':{'ge1':{'info':'not support 2'}}
		}

	t = create_table(dict)
	print t
