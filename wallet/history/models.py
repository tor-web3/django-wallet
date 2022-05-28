from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.
from wallet.models import Token,Address
from wallet.history import constant



class Deposit(models.Model):
    uuid = models.CharField(verbose_name=_("History UUID"),max_length=64,editable=False)
    txid = models.CharField(verbose_name=_('TXID'),max_length=256,editable=False,
                            null=True,default=None,blank=True, unique=True,)
    counterparty = models.ForeignKey(
        get_user_model(),verbose_name=_('Internal CounterParty ID'),
        related_name='wallet_history_deposit',on_delete=models.DO_NOTHING,
        null=True,blank=True,default=None,editable=False
    )
    counterparty_address = models.CharField(
        verbose_name=_("CounterParty Address"), max_length=128,
    )
    deposit_address = models.CharField(
        verbose_name=_("Deposit Address"), max_length=128,
    )
    deposit = models.ForeignKey(
        Address, related_name="wallet_history_deposit",
        on_delete=models.DO_NOTHING,
        null=True,blank=True,default=None,editable=False
    )

    amount = models.DecimalField(verbose_name=_("Amount"),
        decimal_places=8,
        max_digits=32,)

    token = models.ForeignKey(Token,default=None,on_delete=models.CASCADE,editable=False)
    memo = models.CharField(verbose_name=_('Memo'),max_length=128,
                            null=True,blank=True,default="",help_text=_('Label/Tag/Memo'))

    status = models.CharField(
        verbose_name=_('Status'), max_length=32,
        choices=constant.TRANSACTION_STATUS,
        default=constant.SUBMITTED,editable=False,
        null=True,blank=True
    )
    error_info = models.CharField(verbose_name=_("Error Info"),max_length=255,editable=False,
                                  null=True,blank=True,default="")
    
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True,editable=False)
    updated_time = models.DateTimeField(_("Updated Time"), auto_now=True,editable=False)
    finished_time = models.DateTimeField(verbose_name=_("Finished Time"),editable=False,
                                         null=True,blank=True,default=None)
    block_time = models.DateTimeField(verbose_name=_("Block Time"),editable=False,
                                         null=True,blank=True,default=None)

    class Meta:
        ordering = ["-created_time"]



class Deposited(Deposit):
    
    class Meta:
        ordering = ["-created_time"]