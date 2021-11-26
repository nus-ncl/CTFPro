from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import (
   BaseUserManager, User
)

# Create your models here.

class Component(models.Model):
	component_text = models.CharField(max_length=200)
	hostname = models.CharField(max_length=200, default = ' ')
	status = models.CharField(max_length=200, default = ' ')
	def __str__(self):
		return self.component_text


