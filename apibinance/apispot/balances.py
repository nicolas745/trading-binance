
import os
from classenum.env import configenv
class balances():
    def __init__(self,balances) -> None:
        self.wallets = {}
        for balance in balances["balances"]:
           self.wallets[balance['asset']] = balance
    def getwallets(self):
        return self.wallets
    def getactifprincal(self):
        return self.getwallets()[os.getenv(configenv.MONEY_PRINCIPAL.value).upper()]['free']
    def getactifechange(self):
        return self.getwallets()[os.getenv(configenv.MONEY_ECHANGE.value).upper()]['free']