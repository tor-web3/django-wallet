from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect

# Register your models here.
from wallet.history.models import Deposit,Withdraw
from wallet.history import constant

class DepositAdmin(admin.ModelAdmin):

    list_display = (
        "counterparty_address","amount","token",
        "block_time",
        "deposit_address","status",
        "created_time",
    )
    list_filter = ("deposit__user","token__chain")

class WithdrawAdmin(admin.ModelAdmin):
    list_display = (
        "txid","counterparty_address","amount","token","status","updated_time"
    )

    readonly_fields = ("status",)

    change_form_template = "admin/wallet/history/audit_withdraw.html"

    def response_change(self, request, obj):
        if "allow" in request.POST:
            
            matching_names_except_this = self.get_queryset(request).get(pk=obj.id)
            if matching_names_except_this.status != constant.SUBMITTED:
                self.message_user(request, "The order is abnormal and cannot be reviewed")
                return HttpResponseRedirect(".")

            matching_names_except_this.status = constant.AUDITED
            matching_names_except_this.save(update_fields=["status"])
            self.message_user(request, "Allow Withdraw")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Deposit,DepositAdmin)
admin.site.register(Withdraw,WithdrawAdmin)