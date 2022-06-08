from django.contrib import admin

# Register your models here.
from wallet.chainstate.models import *

class RPCAdmin(admin.ModelAdmin):

    list_display = ("chain","company","alias","endpoint","username","password","auth",)
    
class StateAdmin(admin.ModelAdmin):

    list_display = ("address","query_count","balance","is_update","rpc","stop_at","updated_at")

admin.site.register(RPC,RPCAdmin)
admin.site.register(State,StateAdmin)