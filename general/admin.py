from django.contrib import admin
from .models import Producter, Location, Device_type, Internet_Ip, Intranet_Ip
# Register your models here.

admin.site.register(Producter)
admin.site.register(Location)
admin.site.register(Device_type)
admin.site.register(Internet_Ip)
admin.site.register(Intranet_Ip)
