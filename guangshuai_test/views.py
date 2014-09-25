#from django.shortcuts import render
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
from guangshuai_test.creattable import *
# Create your views here.
def index(requst):
	return render_to_response('index.html')

def result(request):
	name = "lijie2"
	dict = { '1.1.1.1':{'ge0':{'rx':1,'tx':2},'ge2':{'rx':2,'tx':3}},
		'2.2.2.2':{'ge1':{'rx':1,'tx':2}}
			}
		
	table = create_table(dict)

	return render_to_response("result.html",{'guangshuai_table':table})





