from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone, datetime_safe as datetime

# Create your models here.
from wallet.models import Token,Address
from wallet.history import constant
from wallet.history.signals import post_withdraw

from uuid import uuid4

from logging import getLogger
logger = getLogger(__name__)


class Deposit(models.Model):
    uuid = models.CharField(verbose_name=_("History UUID"),max_length=64,editable=False,default=None)
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
        help_text=_("Owner of the order"),
        null=True,blank=True,default=None,editable=False
    )

    amount = models.DecimalField(verbose_name=_("Amount"),
        decimal_places=8,
        max_digits=32,)

    token = models.ForeignKey(Token,default=None,on_delete=models.CASCADE)
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

    def __str__(self):
        return self.uuid
    
    def save(self,*args,**kargs):
        try:
            if self.deposit_address:
                self.deposit = Address.objects.get(address=self.deposit_address)
        except Address.DoesNotExist as e:
            logger.error(f"address[{self.deposit_address}] not found.",exc_info=e.args)
            raise e
        if self.uuid is None:
            self.uuid = uuid4()
        adding = self._state.adding
        super().save(*args,**kargs)

        if adding:
            from wallet.history.signals import wallet_address_deposit
            wallet_address_deposit.send(
                    sender=self.__class__,
                    instance = self,
                    from_address = self.counterparty_address,
                    to_address = self.deposit_address,
                    amount = self.amount,
                    token_symbol = self.token.token_symbol,
                    memo = self.memo,
                    user = self.deposit.user
                )


    class Meta:
        ordering = ["-block_time"]
        
        verbose_name = _('Deposit')
        verbose_name_plural = _('Deposit')



class Withdraw(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("User ID"),on_delete=models.CASCADE
    )
    uuid = models.CharField(verbose_name=_("History UUID"),max_length=64,editable=False,default=None)
    txid = models.CharField(verbose_name=_('TXID'),max_length=256,editable=False,
                            null=True,default=None,blank=True, unique=True,)
    counterparty = models.ForeignKey(
        get_user_model(),verbose_name=_('Internal CounterParty ID'),
        related_name='wallet_history_withdraw',on_delete=models.DO_NOTHING,
        null=True,blank=True,default=None,editable=False
    )
    counterparty_address = models.CharField(
        verbose_name=_("CounterParty Address"), max_length=128,
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        decimal_places=8,max_digits=32,
    )

    fee = models.DecimalField(
        verbose_name=_("Fee"),
        decimal_places=8,max_digits=32,
        default=0
    )
    token = models.ForeignKey(Token,default=None,on_delete=models.CASCADE)
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
    success_info = models.TextField(verbose_name=_("Success Info"),editable=False,
                                  null=True,blank=True,default="")
    request_info = models.TextField(verbose_name=_("Request Info"),editable=False,
                                  null=True,blank=True,default="")
    
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True,editable=False)
    updated_time = models.DateTimeField(_("Updated Time"), auto_now=True,editable=False)
    finished_time = models.DateTimeField(verbose_name=_("Finished Time"),editable=False,
                                         null=True,blank=True,default=None)
    block_time = models.DateTimeField(verbose_name=_("Block Time"),editable=False,
                                         null=True,blank=True,default=None)

    def __str__(self):
        return self.uuid
    

    def save(self,*args,**kargs):
        if self.uuid is None:
            self.uuid = uuid4().__str__()        
        super().save(*args,**kargs)

        if self.txid and self.status == constant.WITHDRAWING:
            post_withdraw.send(
                sender      = self.__class__,
                instance    = self,
                txid        = self.txid,
                to_address  = self.counterparty_address,
                amount      = self.amount,
                fee         = self.fee,
                token_symbol= self.token.token_symbol,
                memo        = self.memo,
                user        = self.user
            )
    
    def cancel(self):
        if self.status == constant.SUBMITTED:
            self.status = constant.REJECT
            self.error_info = "user cancel this order"
            self.finished_time = timezone.now()
            self.save(update_fields=["status","error_info","finished_time"])
            return True
        return False
        