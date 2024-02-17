from .simple_earn.flexible import flexible
class simple_earn():
    def __init__(self,base_url,api_secret,api_key) -> None:
        self.base_url = base_url
        self.api_secret = api_secret
        self.api_key = api_key
    def getflexible(self):
        return flexible(self.base_url,self.api_secret,self.api_key)