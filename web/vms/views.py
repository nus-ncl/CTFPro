from django.http import HttpResponse
from django.template import loader
from .forms import NewUserForm, componentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.db import models
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
				auth_login(request, user)
				return redirect("/vms/index.html/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="vms/login.html", context={"login_form":form})


def index(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/index.html', context)
	
def components(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/components.html', context)

def component_form(request):
	if request.method == "POST":
		form = componentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/vms/components.html/')
			
	else:
		form = componentForm()
	return render(request, 'vms/component-form.html', {'form': form})

def pagelogout(request):
	if request.method == "POST":
		logout(request)

		return redirect('/vms/')

	
def challenges(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/challenges.html', context)
	
def dashboard(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/dashboard.html', context)
	
def landpage(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/landpage.html', context)

def monitor(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/monitor.html', context)

def stats(request):
	user = request.user
	
	data = Component.objects.filter(username = user)
	
	context = {'data': data}
	
	return render(request, 'vms/stats.html', context)
	


