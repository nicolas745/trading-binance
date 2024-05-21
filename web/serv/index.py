from flask import Flask, render_template, request, session, redirect
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO
from gnupg import GPG
load_dotenv()
import subprocess
import time
import threading
import random
import string

class index():
    def __init__(self, app: Flask, socketio: SocketIO) -> None:
        self.passwd = None
        self.time = True
        t = threading.Thread(target=self.passwdtime)
        t.start()
        
        @app.get("/")
        def getlogin():
            if session.get("user"):
                return redirect("/panel")
            return render_template('index.html')
        
        @app.post("/")
        def postlogin():
            if session.get("user"):
                return redirect("/panel")
            if request.method == 'POST':
                if self.passwd is not None and request.form.get('passwd') == self.passwd:
                    session['user'] = 1
                    self.passwd = None
                    return redirect("/panel")
            return render_template('index.html')
        
        @app.get('/passwd')
        def getpasswd():
            gpg = GPG()
            with open('gpg/key.public', 'r') as f:
                public_key = f.read()
                import_result = gpg.import_keys(public_key)
            fingerprint = None
            for key in import_result.results:
                fingerprint = key['fingerprint']
            self.passwd = self.generate_password(1000)
            encrypt_result = subprocess.run(['gpg', '-a', '--encrypt', '--always-trust', '--recipient', fingerprint], input=self.passwd, text=True, capture_output=True)
            self.time = False
            return str(encrypt_result.stdout)
    
    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation + "αβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσΤτΥυΦφΧχΨψΩωàâéèêëîïôùûüÿçÀÂÉÈÊËÎÏÔÙÛÜŸÇ"
        password = ''.join(random.choice(characters) for i in range(length))
        return password
    
    async def passwdtime(self):
        while True:
            while self.time:
                pass
            self.time = True
            time.sleep(60)
            self.passwd = None
