#from django.shortcuts import render
from django.http import HttpResponse
from guangshuai_test.models import Guangshuai 
from django.template import Context,loader
from django.shortcuts import render_to_response
# Create your views here.
def index(request):
	#return HttpResponse("Hello LiJie!!!,you success!!")
	return render_to_response('index.html',{'name':'lijie','age':'15'})


def search(requst):
	if 'q' in request.GET:
		message = 'You searched for:%r'%request.GET['q']
	else:
		message = 'You submitted an empty form.'
	return HttpResponse(message)
