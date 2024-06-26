from flask import Flask
from flask_socketio import SocketIO
import os
import importlib
app = Flask(__name__)
from classenum.env import configenv
app.secret_key = os.urandom(24).hex()
Socketio =SocketIO()
Socketio.init_app(app)
class main():
    def __init__(self) -> None:
        directory = "web/serv"
        for filename in os.listdir(directory):
            if filename.endswith(".py"):  # Assurez-vous que vous ne traitez que les fichiers Python
                module_path = os.path.join(directory, filename)
                # Importez dynamiquement le module
                module = importlib.import_module(module_path[:-3].replace("/","."))
                # Parcourez les objets dans le module
                for name in dir(module):
                    obj = getattr(module, name)
                    # Vérifiez si l'objet est une classe
                    if isinstance(obj, type):
                        if(obj.__module__==module_path[:-3].replace("/",".")):
                            obj(app,Socketio)
def run():
    if __name__ == 'web.main':
        args = {
            'app':app,
            'port':os.getenv(configenv.PORT.value),
            'debug':False,
            'host':os.getenv(configenv.HOST.value)
        }
        if os.getenv(configenv.SSL.value)!="false":
            args['ssl_context'] = (os.getenv(configenv.SSLCERFILE.value),os.getenv(configenv.SSLKEYFILE.value))
            Socketio.run(**args)
        else:
            Socketio.run(**args)