from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Component


def login(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/login.html', context) 

def index(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/index.html', context)
	
	
def components(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/components.html', context)
	
def challenges(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/challenges.html', context)
	
def dashboard(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/dashboard.html', context)
	
def landpage(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/landpage.html', context)

def monitor(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/monitor.html', context)

def stats(request):
	c_list = Component.objects.all()
	
	context = {'c_list': c_list}
	
	return render(request, 'vms/stats.html', context)
	


