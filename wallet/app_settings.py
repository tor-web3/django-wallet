

class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings

        getter = getattr(
            settings,
            "WALLET_SETTING_GETTER",
            lambda name, dflt: getattr(settings, name, dflt),
        )
        return getter(self.prefix + name, dflt)

    @property
    def USER_MAIN_PUBLIC_KEY(self):
        return self._setting("USER_PUBLIC_KEY", True)

    @property
    def DEFAULT_WALLET(self):
        return self._setting("DEFAULT_WALLET", 
        {
            "mnemonic":"amount frame elevator power bronze primary frown output gown negative merge borrow",
            "root_key": "xprv9s21ZrQH143K2p4jWjx3KW7QnerUMSQRvSowuYxok3Tg4A74CCe4LsiKiBzimxk5r5z1eHzEFr3JX6PrALXoJT2YjP5Sz53RMJKqDpj3C8G",
            # m/44'/195'/0'
            "trx_account_private_key":"xprv9yCUi5XAAjEbgQFjG6g95mPZJ7ZJ7e3hmKJVoHQLtKtWXFUeLHYmFw2y2AiABnRBeUoqxYTo6EJREqM6RtAgT6Nub9Sk3MPHMCD4iCRtXDt",
            "trx_account_public_key":"xpub6CBq7b4416ntttLCN8D9SuLHr9PnX6mZ8YE6bfoxSfRVQ3onsps1ojMSsSvAPEaygKStBQxiMEfBzysfqPfp2t7oyXmcDzxVHUgsEig8RrV",
            # m/44'/60'/0'
            "eth_account_private_key":"xprv9xjdefLiehKnsqybUs7URSVdZmXFFwXLbjr2S2bXWu2FMURmkZx8mLHY3rnb7kFBw8izFWfJ8dHc7b5EBDFrsvCbLBohEHVecSsdLCMQ6Mc",
            "eth_account_public_key":"xpub6Biz4AscV4t66L44ateUnaSN7oMjfQFBxxmdER195EZEEGkvJ7GPK8c1u6ipVUVMWxEJvGSjhiGLvFQrUAXoZLwHPLtQCsuWbEECUHCRdXW",
            # m/44'/60'/0'
            "xmr_secret_view_key":"bdb9bc040c690bfccc6f4fdca66a705a046ac3402ccc2c38bb72f2aef3768900",
            "xmr_address":"48NLPW7hugSV3MuXcLKmLzTvyZ4twYu9sWza8zz5Q6ueiocKWvz6QHUSxEwdTWgidNYv4C5AiGLFc4vCNU7bdkRf5R9BRob",
        })
    
    def ACCOUNT_PUBLIC_KEY(self,chain_symbol) -> str:
        chain_symbol = chain_symbol.lower()
        return self.DEFAULT_WALLET[f'{chain_symbol}_account_public_key']

    @property
    def TRX_ACCOUNT_PUBLIC_KEY(self):
        return self.DEFAULT_WALLET['trx_account_public_key']
    @property
    def XMR_SECRET_VIEW_KEY(self):
        return self.DEFAULT_WALLET['xmr_secret_view_key']
    @property
    def XMR_ADDRESS(self):
        return self.DEFAULT_WALLET['xmr_address']

# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys  # noqa


app_settings = AppSettings("WALLET_")
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
