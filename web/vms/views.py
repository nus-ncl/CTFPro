from django.http import HttpResponse
from django.template import loader
from .forms import NewUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import Component

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Registration successful." )
			return redirect("/vms/login.html/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="vms/register.html", context={"register_form":form})

def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/vms/index.html/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="vms/login.html", context={"login_form":form})


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
	


