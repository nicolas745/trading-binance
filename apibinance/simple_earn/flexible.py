from binance.client import Client
class flexible:
    def __init__(self, client:Client) -> None:
        self.client =client
    def getmyposition(self):
        return self.client.get_simple_earn_flexible_product_position()
    def getdispo(self):
        return self.client.get_simple_earn_flexible_product_list()
    def retir(self, crypto, valeur):
        data = self.getmyposition()
        for position in data["rows"]:
            if position["asset"] == crypto and float(position["totalAmount"]) >= valeur:
                productId = position["productId"]
                res = self.client.redeem_simple_earn_flexible_product(amount=valeur, product_id=productId)
                return res["success"]
        return False
    def ajouter(self,crypto,valeur):
        data = self.getdispo()
        for donne in data["rows"]:
            if donne["asset"] == crypto:
                productId = donne["productId"]
                if float(donne["minPurchaseAmount"]) > valeur:
                    return False
        res=self.client.subscribe_simple_earn_flexible_product(amount=0.1, product_id=productId)
        return res["success"]