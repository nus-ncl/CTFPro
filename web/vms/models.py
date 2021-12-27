
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import (
    BaseUserManager, User
)

# Create your models here.


class Component(models.Model):
    component_id = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=45)
    hostname = models.CharField(max_length=45)
    url_access = models.CharField(db_column='URL_access', max_length=45)  # Field name made lowercase.
    username = models.CharField(max_length=45)


