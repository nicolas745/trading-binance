from binance.client import Client, AsyncClient
class flexible:
    def __init__(self, client:Client|AsyncClient) -> None:
        self.client =client
    def getmyposition(self):
        return self.client.get_simple_earn_flexible_product_position()
    def getmyposamount(self,monney:str):
        for flex in self.getmyposition()["rows"]:
            if(flex['asset']==monney.upper()):
                return flex["totalAmount"]
    def retir(self, crypto, valeur):
        data = self.getmyposition()
        for position in data["rows"]:
            if position["asset"] == crypto and float(position["totalAmount"]) >= valeur and position["minPurchaseAmount"]<=valeur:
                productId = position["productId"]
                res = self.client.redeem_simple_earn_flexible_product(amount=valeur, product_id=productId)
                return res["success"]=="true"
        return False
    def ajouter(self,crypto,valeur):
        data = self.getmyposition()
        for donne in data["rows"]:
            if donne["asset"] == crypto:
                productId = donne["productId"]
                if float(donne["minPurchaseAmount"]) > valeur:
                    res=self.client.subscribe_simple_earn_flexible_product(amount=valeur, product_id=productId)
                    return res["success"]=="true"
        return False