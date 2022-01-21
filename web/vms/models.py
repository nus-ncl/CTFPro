
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import BaseUserManager, User, AbstractUser
from django.conf import settings

# Create your models here.


class Component(models.Model):
    Type = models.CharField(max_length=45)
    hostname = models.CharField(max_length=45)
    component_id = models.AutoField(primary_key=True)
    url_access = models.CharField(db_column='URL_access', max_length=45)  # Field name made lowercase.
    username = models.CharField(max_length=45)
    state = models.CharField(max_length=45)


class User(AbstractUser):
    institution = models.CharField(max_length=300, blank=True)
