import admin_interface.apps
from django.contrib import admin
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
