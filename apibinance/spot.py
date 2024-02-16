from .apispot.balances import balances
class spot:
    def __init__(self,data) -> None:
        self.data = data
    def getdata(self):
        return self.data
    def getbalances(self) -> balances:
        return balances(self.data["balances"])