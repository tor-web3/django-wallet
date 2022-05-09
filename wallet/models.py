from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.
from .constant import *

class Chain(models.Model):
    chain_name = models.CharField(verbose_name=_("Chain Name"), max_length=32, default="Tron")
    chain_network = models.CharField(verbose_name=_("Chain Network"), max_length=32)
    chain_symbol = models.CharField(verbose_name=_("Chain Token Symbol"), max_length=32, default="TRX")
    
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("Updated Time"), auto_now=True)

    explorer_url = models.CharField(verbose_name=_("Explorer URL"),max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.chain_name}[{self.chain_network}]"

    class Meta:
        verbose_name = _('chain')
        verbose_name_plural = _('chain')

class Pubkey(models.Model):
    user = models.ForeignKey(get_user_model(),related_name='wallet_pubkey',blank=True,null=True,verbose_name=_("User ID"),on_delete=models.CASCADE)
    public_key = models.CharField(verbose_name=_("Account Extended Public Key"),max_length=128,unique=True)

    chain = models.ForeignKey(Chain, on_delete=models.SET_NULL,null=True)
    
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True)
    
    def __str__(self):
        return f"Public Key@{self.user}[{self.chain}]"
    
    class Meta:
        verbose_name = _('public key')
        verbose_name_plural = _('public key')



class Token(models.Model):
    chain = models.ForeignKey(Chain, on_delete=models.SET_NULL,null=True)
    
    contract_address = models.CharField(verbose_name=_("Contract Address"),
                                        max_length=128, blank=True, null=True,)
    token_symbol = models.CharField(verbose_name=_("Token Symbol"), max_length=32, null=True)
    token_name = models.CharField(verbose_name=_("Token Name"), max_length=64, null=True)
    token_decimal = models.SmallIntegerField(verbose_name=_("Token Decimal"),default=6)

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this address should be treated as active. "
            "Unselect this instead of deleting address."
        ),
    )
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("Updated Time"), auto_now=True)

    def __str__(self) -> str:
        return f"{self.token_name}"

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')
        unique_together = [("token_symbol", "contract_address")]



class Address(models.Model):
    user = models.ForeignKey(get_user_model(),related_name='wallet_address',null=True,verbose_name=_("User ID"),
                            on_delete=models.CASCADE)
    pubkey = models.ForeignKey(Pubkey,related_name="wallet_address",verbose_name=_("Public Key"),
                            on_delete=models.CASCADE)
    
    chain = models.ForeignKey(Chain, related_name="wallet_address",on_delete=models.SET_NULL, null=True)

    label = models.CharField(verbose_name=_('Label'),max_length=128,
                            null=True,blank=True,help_text=_('Label/Tag/Memo'))
    index = models.IntegerField(verbose_name=_("Inedx"),default=0)
    address = models.CharField(
        verbose_name=_("address"),unique=True,
        max_length=128, default=_("Temporary discontinuation of service")
    )
    type = models.CharField(verbose_name=_("Address Type"), max_length=32,
                            choices=ADDRESS_TYPE)

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this address should be treated as active. "
            "Unselect this instead of deleting address."
        ),
    )
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True,editable=False)


    def __str__(self):
        return f"{self.address}"
    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
