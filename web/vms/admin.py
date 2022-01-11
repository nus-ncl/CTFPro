from django.contrib import admin

# Register your models here.

from .models import Component, User

admin.site.register(Component)

admin.site.register(User)
