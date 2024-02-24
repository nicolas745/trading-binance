from flask import Flask, render_template, request,session, redirect
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO
from gnupg import GPG
load_dotenv()
import subprocess
import time
import random
import string
import threading
class index():
    def __init__(self,app:Flask,socketio:SocketIO) -> None:
        self.passwd = None
        self.time=True
        t = threading.Thread(target=self.passwdtime)
        t.start()
        @app.get("/")
        def getlogin():
            #session["user"] = 1
            if(session.get("user")):
                return redirect("/panel")
            return render_template('index.html')
        @app.post("/")
        def postlogin():
            if(session.get("user")):
                return redirect("/panel")
            if request.method == 'POST':
                if self.passwd != None:
                    if(request.form.get('passwd')==self.passwd):
                        session['user'] = 1
                        self.passwd = None
                        return redirect("/panel")
                pass
            return render_template('index.html')
        @app.get('/passwd')
        def getpasswd():
            gpg = GPG()

            # Importer la clé publique à partir du fichier
            with open('gpg/key.public', 'r') as f:
                public_key = f.read()
                import_result=gpg.import_keys(public_key)
            fingerprint = None
            for key in import_result.results:
                fingerprint = key['fingerprint']
            self.passwd=self.generer_chaine(1000)
            encrypt_result = subprocess.run(['gpg', '-a', '--encrypt', '--always-trust', '--recipient', fingerprint], input=self.passwd, text=True, capture_output=True)
            # encrypted_data=gpg.encrypt(self.passwd,fingerprint)
            self.time = False
            return str(encrypt_result.stdout)
    def generer_chaine(self,longueur):
        # Définir les caractères spéciaux
        caracteres_speciaux = string.punctuation
        # Définir tous les caractères possibles (lettres, chiffres et caractères spéciaux)
        tous_caracteres = string.ascii_letters + string.digits + caracteres_speciaux
        # Générer une chaîne de la longueur spécifiée
        chaine = ''.join(random.choice(tous_caracteres) for _ in range(longueur))
        return chaine
    async def passwdtime(self):
        while(True):
            while(self.time):
                pass
            self.time = True
            time.sleep(60)
            self.passwd = None