from django.contrib import admin

# Register your models here.
from wallet.chainstate.models import *

class RPCAdmin(admin.ModelAdmin):

    list_display = ("chain","company","alias","endpoint","username","password","auth",)
    
class StateAdmin(admin.ModelAdmin):

    list_display = ("address","balance","next_time","is_active","rpc","next_time")

admin.site.register(RPC,RPCAdmin)
admin.site.register(State,StateAdmin)