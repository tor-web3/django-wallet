from django.dispatch import Signal


# 钱包地址充值信号
# sender=self.__class__,
# instance = self,
# from_address = self.counterparty_address,
# to_address = self.deposit_address,
# amount = self.amount,
# token_symbol = self.token.token_symbol,
# memo = self.memo,
# user = self.deposit.user
wallet_address_deposit = Signal()

# pre_withdraw = Signal()
post_withdraw = Signal()
