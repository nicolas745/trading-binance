class balances():
    def __init__(self,balances) -> None:
        self.wallets = {}
        for balance in balances:
            self.wallets[balance['asset']] = balance
    def getwallets(self):
        return self.wallets