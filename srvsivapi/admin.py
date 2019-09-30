from django.contrib import admin

from .models import Employee,SRV,SIV,Items

admin.site.register([Employee,SIV,SRV,Items])

# Register your models here.
