from .simple_earn.flexible import flexible
from binance.client import Client
class simple_earn():
    def __init__(self,client) -> None:
        self.client = client
    def getflexible(self):
        return flexible(self.client)