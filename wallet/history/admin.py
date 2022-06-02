from django.contrib import admin

# Register your models here.
from wallet.history.models import Deposit

class DepositAdmin(admin.ModelAdmin):

    list_display = (
        "counterparty_address","amount","token",
        "block_time",
        "deposit_address","status",
        "created_time",
    )
    list_filter = ("deposit__user","token__chain")


admin.site.register(Deposit,DepositAdmin)