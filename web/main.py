from flask import Flask
import os
import importlib
app = Flask(__name__)
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
                            print(obj)
                            obj(app)
def run():
    if __name__ == 'web.main':
        app.run(debug=True)