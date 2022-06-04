from django.dispatch import Signal


# 钱包地址充值信号
# sender=self.__class__,
# instance = self,
# amount = self.amount,
# token_symbol = self.token.token_symbol
# user = self.deposit.user
wallet_address_deposit = Signal()
