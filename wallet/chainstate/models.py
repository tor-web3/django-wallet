from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
# Create your models here.
from wallet.models import Chain,CreateUpdateTracker,Address
from wallet.chainstate.constant import *
from wallet.chainstate.signals import wallet_address_updated

from typing import Any, Optional,List

class RPC(CreateUpdateTracker):
    chain = models.ForeignKey(Chain, related_name='wallet_chainstate_rpc', on_delete=models.CASCADE)
    company = models.CharField(verbose_name=_("company"),max_length=128)
    alias = models.CharField(verbose_name=_("alias"),max_length=128,blank=True,null=True,)
    endpoint = models.CharField(verbose_name=_("endpoint"),max_length=128)
    username = models.CharField(verbose_name=_("username"),max_length=128,blank=True,null=True,)
    password = models.CharField(verbose_name=_("password"),max_length=128,blank=True,null=True,)
    auth = models.CharField(verbose_name=_("auth"),max_length=128,choices=AUTH_TYPE,default=NORMAL)
    
    def __str__(self):
        return f"{self.alias}-[{self.company}]"

    class Meta:
        verbose_name = _('RPC')
        verbose_name_plural = _('RPC')


class StateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('updated_at')

class State(CreateUpdateTracker):
    
    def __init__(self,*args,**kwargs):
        self.update_fields = []
        super(State,self).__init__(*args,**kwargs)
        
    objects = StateManager()

    address = models.OneToOneField(Address, related_name="wallet_chainstate_state",on_delete=models.CASCADE)
    usdt_balance = models.DecimalField(
        verbose_name=_('usdt balance'),
        max_digits=32,decimal_places=8,
        default=0,
    )
    stop_at = models.DateTimeField(
        _("Stop Time"),editable=False,
        help_text=_(
            "When to stop the test"
        )
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),default=True,
        help_text=_(
            "Whether it is necessary to detect the operating status of the address"
        )
    )
    is_update = models.BooleanField(
        verbose_name=_('update'),default=False,
        help_text=_(
            "Status of address update"
        )
    )
    query_count = models.IntegerField(verbose_name=_('query count'),default=0)
    rpc = models.ForeignKey(
        RPC, related_name="wallet_chainstate_state", 
        on_delete=models.CASCADE, null=True
    )

    @property
    def balance(self):
        return self.usdt_balance
    @balance.setter
    def balance(self,value:Decimal):
        if self.usdt_balance != value and value != None:
            self.usdt_balance = value
            self.is_update = True
            self.update_fields = ['usdt_balance','is_update']
            return self.usdt_balance
        return None

    def active(self):
        from django.utils import timezone        
        now = timezone.now()
        self.stop_at = now + timezone.timedelta(hours=24,minutes=0,seconds=0)
        self.is_active = True
        self.save(update_fields=['stop_at','is_active'])
        

    def flush(self):
        self.query_count = self.query_count + 1
        self.update_fields.append('query_count')

        # 检查地址是否仍然活跃
        from django.utils import timezone
        now = timezone.now()
        if self.stop_at < now:
            self.is_active = False
            self.update_fields.append('is_active')
        
        # 更新地址信息
        fields = list(set(self.update_fields))
        self.save(update_fields=fields)
        if self.is_update:
            wallet_address_updated.send(
                sender=self.__class__,
                instance = self,
            )

    def __str__(self):
        return f"{self.is_update}"

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('Status')
