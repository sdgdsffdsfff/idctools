#!/usr/bin/python

def create_table(dict):
	
	switch_list = dict.keys()
	#the function will eventually return the string opject table to the html
	table = ""
	#count numbers of every switch
	interface_number = []
	for i in switch_list:
		interface_number.append(str(len(dict[i])))	
	colors = ["danger","info"]

		
	#create table with forloop
	for i in range(len(switch_list)):
		#define the color 
		if i % 2 == 0 :
			color = colors[0]
		else:
			color = colors[1]
		#identify how many numbers does the switch has
		#if interface_number >1 ,merge the row 
		if interface_number[i] > 1:
			table += '<tr class='+color+'><td rowspan="' + interface_number[i] +'">'+switch_list[i]+'</td>'
			interface = dict[switch_list[i]].keys()
			table += '<td>'+interface[0]+'</td>'+'<td>'+str(dict[switch_list[i]][interface[0]]['rx'])+'</td>'+'<td>'+str(dict[switch_list[i]][interface[0]]['tx'])+'</td></tr>'
			interface = interface[1:]
			for j in interface:
				table += '<tr class='+color+'><td>'+j+'</td>'+'<td>'+str(dict[switch_list[i]][j]['rx'])+'</td>'+'<td>'+str(dict[switch_list[i]][j]['tx'])+'</td></tr>'	
			
			

		else:
			interface = dict[switch_list[i]].keys()
			table += '<tr class='+color+'><td>'+switch_list[i]+'</td>'+'<td>'+interface[0]+'</td>'+'<td>'+str(dict[switch_list[i]][interface[0]]['rx'])+'</td>'+'<td>'+str(dict[switch_list[i]][interface[0]]['tx'])+'</td></tr>'
	return table
###############################################################################################################################
if __name__ == "__main__":
	dict = {'1.1.1.1':{'ge0':{'rx':2,'tx':3},'ge1':{'rx':1,'tx':5},'ge2':{'rx':1,'tx':3}},'2.2.2.2':{'ge3':{'rx':4,'tx':5},'ge1':{		'rx':1,'tx':2}},'3.3.3.3':{'tge3':{'rx':-1,'tx':-2.5},'Tge2':{'rx':0.1,'tx':2},'tge1':{'rx':1,'tx':2},'tge0':{'rx':1,'tx':2}		},'4.4.4.4':{'ge1':{'rx':1,'tx':2}}
		}

	t = create_table(dict)
	print t
