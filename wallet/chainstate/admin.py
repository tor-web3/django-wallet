from django.contrib import admin
from django.utils import timezone

# Register your models here.
from wallet.chainstate.models import *

class RPCAdmin(admin.ModelAdmin):

    list_display = ("chain","company","alias","endpoint","username","password","auth",)
    
class StateAdmin(admin.ModelAdmin):

    actions = ['make_active',"make_update","make_inactivity"]

    @admin.action(description='Mark selected state as inactivity')
    def make_inactivity(self, request, queryset):
        now = timezone.now()
        queryset.update(is_active=False,stop_at=now)

    @admin.action(description='Mark selected state as activeted')
    def make_active(self, request, queryset):
        now = timezone.now()
        stop_at = now + timezone.timedelta(hours=24,minutes=0,seconds=0)
        queryset.update(is_active=True,stop_at=stop_at)
        
    @admin.action(description='Mark selected state as update')
    def make_update(self, request, queryset):
        queryset.update(is_update=False,usdt_balance=0)

    list_display = ("address","query_count","balance","is_update","is_active","rpc","stop_at","updated_at")

admin.site.register(RPC,RPCAdmin)
admin.site.register(State,StateAdmin)