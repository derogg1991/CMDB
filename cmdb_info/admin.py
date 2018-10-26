from django.contrib import admin
from cmdb_info.models import Pc_Info, Server_Info, Network_Device_Info, Nat_Info


# Register your models here.


class Pc_InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['sn', 'ecar_no', 'ip', 'user', 'location', 'status']}),
        ('时间信息', {'fields': ['create_date', 'modi_time']}),
        ('详细信息', {'fields': ['producter', 'type', 'cpu', 'mem', 'disk', 'remark']})
    ]
    list_display = ('sn', 'type', 'ecar_no', 'ip', 'user', 'create_date', 'modi_time', 'location', 'status')
    list_per_page = 50
    list_filter = ['modi_time', 'location', 'status', 'type']
    search_fields = ['ecar_no', 'ip', 'sn', 'user', 'create_date']

class Server_InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['sn', 'ecar_no', 'ip', 'user', 'location', 'status']}),
        ('时间信息', {'fields': ['create_date', 'modi_time']}),
        ('详细信息', {'fields': ['producter', 'type', 'cpu_core', 'cpu_thread', 'cpu_no', 'mem', 'disk', 'env', 'remark' ]})
    ]
    list_display = ('sn', 'type', 'ecar_no', 'ip', 'user', 'create_date', 'modi_time', 'location', 'status')
    list_per_page = 50
    list_filter = ['modi_time', 'location', 'status', 'type']
    search_fields = ['ecar_no', 'ip', 'sn', 'user', 'create_date']

class Network_InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['sn', 'ecar_no', 'ip', 'user', 'location', 'status']}),
        ('时间信息', {'fields': ['create_date', 'modi_time']}),
        ('详细信息', {'fields': ['producter', 'type',  'port', 'remark' ]})
    ]
    list_display = ('sn', 'type', 'ecar_no', 'ip', 'user', 'create_date', 'modi_time', 'location', 'status')
    list_per_page = 50
    list_filter = ['modi_time', 'location', 'status', 'type']
    search_fields = ['ecar_no', 'ip', 'sn', 'user', 'create_date']

admin.site.register(Pc_Info, Pc_InfoAdmin)
admin.site.register(Server_Info, Server_InfoAdmin)
admin.site.register(Network_Device_Info, Network_InfoAdmin)
admin.site.register(Nat_Info)
