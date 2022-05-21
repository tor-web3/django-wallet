from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from wallet.models import Chain,CreateUpdateTracker,Address
from wallet.chainstate.constant import *

class RPC(CreateUpdateTracker):
    chain = models.ForeignKey(Chain, related_name='wallet_rpc', on_delete=models.CASCADE)
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
        return super().get_queryset().filter(is_active=True)

class State(CreateUpdateTracker):
    objects = StateManager()

    address = models.ForeignKey(Address, related_name="wallet_state",on_delete=models.CASCADE)
    balance = models.JSONField(verbose_name=_('balance'))
    next_time = models.DateTimeField(
        _("Created Time"),editable=False,
        auto_now=True,
        help_text=_(
            "When to run the next test"
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
    rpc = models.ForeignKey(RPC, related_name="wallet_state", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.is_update}"

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('Status')
