from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

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
    list_filter = ("token__chain",)

class WithdrawAdmin(admin.ModelAdmin):
    list_display = (
        "txid","counterparty_address","amount","token","status","updated_time"
    )

    readonly_fields = ("status","txid")

    change_form_template = "admin/wallet/history/audit_withdraw.html"

    def response_change(self, request, obj):
        if "audit" not in request.POST \
            and "withdrawing" not in request.POST \
            and "refuse" not in request.POST:
            return super().response_change(request, obj)

        matching_names_except_this = self.get_queryset(request).get(pk=obj.id)
        status = matching_names_except_this.status

        # 审核提币
        if "audit" in request.POST and status == constant.SUBMITTED:
            matching_names_except_this.status = constant.AUDITED
        # 提币遇到错误,人工提币
        elif "withdrawing" in request.POST and status == constant.ERROR:
            matching_names_except_this.status = constant.WITHDRAWING
        # 人工审核拒绝提币
        elif "refuse" in request.POST and \
            (status == constant.SUBMITTED or status == constant.ERROR):
            matching_names_except_this.status = constant.REJECT
        else :
        # 非预期的处理类型
            self.message_user(request, _("The order is abnormal and cannot be reviewed"),messages.ERROR)
            return HttpResponseRedirect(".")

        matching_names_except_this.save(update_fields=["status"])
        self.message_user(request, _("Success"),messages.SUCCESS)
        return HttpResponseRedirect("..")



admin.site.register(Deposit,DepositAdmin)
admin.site.register(Withdraw,WithdrawAdmin)