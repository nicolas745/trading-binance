from sql.trading import TradingDatabase
from classenum.sql import enumsql
from classenum.env import configenv
from datetime import datetime
import os
import numpy as np
from flask_socketio import SocketIO
from binance.client import AsyncClient
from apibinance.spot import spot
from apibinance.simpleearn import simple_earn
from datetime import datetime, timedelta
from .order import orders as buysell
import json
res = True
class bot:
    def __init__(self, db:TradingDatabase,client:AsyncClient) -> None:
        self.db = db
        self.client = client
        self.moneyprincipal= os.getenv(configenv.MONEY_PRINCIPAL.value)
        self.moneyechange= os.getenv(configenv.MONEY_ECHANGE.value)
        self.date = enumsql.DATE.value
        self.res = True
        self.sellprix = 0
        self.filejson =  "jsondate.json"
        self.time = 0
    def verifier_ou_creer_fichier(self,fichier):
        # Vérifier si le fichier existe
        if not os.path.exists(fichier):
            # Créer un fichier JSON vide
            with open(fichier, 'w') as f:
                json.dump([], f, indent=4)
    def condition_ma(self,fichier):
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                donnees = json.load(f)
                prix = [d['prix'] for d in donnees]

                if len(prix) >= 200:
                    # Calcul de MA100 et MA200
                    ma100 = np.mean(prix[-100:])
                    ma200 = np.mean(prix[-200:])
                    difference = ma100 - ma200

                    # Calcul de la dérivée de la différence
                    if len(prix) > 200:
                        ma100_past = np.mean(prix[-101:-1])
                        ma200_past = np.mean(prix[-201:-1])
                        difference_past = ma100_past - ma200_past
                        derivee_difference = difference - difference_past
                    else:
                        derivee_difference = 0

                    # Vérification des conditions
                    return difference < 0 or derivee_difference < 0 or derivee_difference != 0
        return False
    def date_plus_recente(self, fichier):
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                donnees = json.load(f)
                if donnees:
                    date_recente = donnees[-1]['date']
                    date_recente = datetime.strptime(date_recente, '%Y-%m-%d').date()
                    date_aujourdhui = datetime.now().date()

                    return date_recente == date_aujourdhui
        return False
    def ajouter_donnee_json(self,fichier, prix):
        # Charger les données existantes
        if os.path.exists(fichier):
            with open(fichier, 'r') as f:
                donnees = json.load(f)
        else:
            donnees = []
        nouvelle_donnee = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "prix": prix
        }
        donnees.append(nouvelle_donnee)

        # Limiter à 300 enregistrements
        if len(donnees) > 300:
            donnees.pop(0)

        # Sauvegarder dans le fichier
        with open(fichier, 'w') as f:
            json.dump(donnees, f, indent=4)
    def start(self, actifprix,Socketio:SocketIO):
        self.verifier_ou_creer_fichier(fichier=self.filejson)
        executorder=0
        actifprix = float(actifprix)
        if( not self.date_plus_recente(self.filejson)):
            self.ajouter_donnee_json(self.filejson,actifprix)
        orders = self.db.get_all_orders()
        if self.sellprix < actifprix/1.01:
            self.sellprix = actifprix/1.01
        elif actifprix <self.sellprix:
            self.sellprix = actifprix
        if orders.__len__():
            if self.condition_ma(self.filejson):
                for order in orders:
                    pricipal= order[self.moneyprincipal]
                    actif=order[self.moneyechange]
                    lastdate=datetime.strptime(order[self.date], "%Y-%m-%dT%H:%M").timestamp()
                    nowdate = datetime.now().timestamp()
                    defdate=nowdate-lastdate
                    prix = pricipal/actif
                    newprix = prix * pow(1 + 0.001, 2) * pow(1 + 0.06 / (365 * 24 * 60 * 60), defdate)
                    pourcentage=(pricipal+((float(actifprix)-newprix)*actif))/pricipal-1
                    if 0.011<pourcentage:
                        if(executorder<4):
                            executorder+=1
                            if(actifprix<=self.sellprix):
                                buysell(self.client).sell(Socketio,order)
        user=self.db.get_portfolio_data()
        self.time=(datetime.now().timestamp()-datetime.strptime(user[self.date], "%Y-%m-%dT%H:%M").timestamp())
        if(12*60*60<self.time):
            buy=10
            nborder =float(user[enumsql.NBEXORDER.value])
            nborderdouble=float(user[enumsql.NBEXORDERDOUBLE.value])
            moneyprincipal= float(user[self.moneyprincipal])
            nborder=nborder+0.5 
            if(nborder<nborderdouble):
                nborderdouble=0
            if(512<nborder):
                nborderdouble=0
                nborder=0
            if(moneyprincipal/5<nborder):
                nborderdouble=0
                nborder=0
            newbuy=buy*pow(1.01,nborderdouble)
            if(newbuy<moneyprincipal):
                self.db.updatedate()
                quantite = newbuy/float(actifprix)
                res=spot(self.client).buy_market(quantite,actifprix)
                if res:
                    self.db.editportfolioorder(nborder,nborderdouble+1)
                    Socketio.emit("add",{
                        self.moneyprincipal:res[self.moneyprincipal],
                        self.moneyechange:res[self.moneyechange]
                    })
    def getsellprix(self):
        return self.sellprix
    def getbuytime(self):
        return str(timedelta(seconds=12*60*60-self.time))