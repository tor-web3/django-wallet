from django.contrib import admin
from wallet.models import *
# Register your models here.

class PubkeyAdmin(admin.ModelAdmin):
    list_display = ("user","public_key","chain",)
    search_fields = ("public_key",)
    ordering = ('-created_at',)
    empty_value_display = '-'
    
    # def has_add_permission(self, request, *args, **kwargs):
    #     return False
    # def has_change_permission(self, request, *args, **kwargs):
    #     return False

class ChainAdmin(admin.ModelAdmin):
    list_display = ("chain_name","chain_network","chain_symbol","created_at","updated_at","explorer_url")
    search_fields = ("chain_name", "chain_symbol")
    ordering = ('-updated_at',)
    empty_value_display = '-'

class TokenAdmin(admin.ModelAdmin):
    list_display = ("chain","contract_address","token_symbol","token_name","is_active","created_at","updated_at")
    search_fields = ("contract_address", "token_symbol")
    ordering = ('-updated_at',)
    list_editable = ['is_active']
    empty_value_display = '-'


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user","pubkey","index",
        'address','is_active',
        'created_at',
    )
    search_fields = ('address',)
    #list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 25
    #ordering设置默认排序字段，负号表示降序排序
    ordering = ('-created_at',)

    # list_editable 设置默认可编辑字段
    list_editable = ['is_active']
    # 对日期进行分类
    # date_hierarchy = 'deposited_time'

    # 字段为空时的默认显示
    empty_value_display = '-'
    
    # def has_add_permission(self, request, *args, **kwargs):
    #     return False
    # def has_change_permission(self, request, *args, **kwargs):
    #     return False
    
class RPCAdmin(admin.ModelAdmin):

    list_display = ("chain","company","alias","endpoint","username","password","auth",)
    
class StateAdmin(admin.ModelAdmin):

    list_display = ("address","balance","next_time","is_active","rpc",)

admin.site.register(RPC,RPCAdmin)
admin.site.register(State,StateAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Chain,ChainAdmin)
admin.site.register(Token,TokenAdmin)
admin.site.register(Pubkey,PubkeyAdmin)