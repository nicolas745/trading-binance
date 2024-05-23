from .simple_earn.flexible import flexible
from api.binance.client import Client,AsyncClient
class simple_earn():
    def __init__(self,client:Client|AsyncClient) -> None:
        self.client = client
    def getflexible(self):
        return flexible(self.client)