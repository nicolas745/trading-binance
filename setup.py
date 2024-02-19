#!.venv/bin/python3
import os
from classenum.env import configenv
from dotenv import load_dotenv
load_dotenv()
class Config:
    def __init__(self):
        table = configenv._member_names_
        self.env = {}
        for tab in table:
            self.env[configenv._member_map_[tab].value] = os.getenv(configenv._member_map_[tab].value)
    def get_user_input(self, variable_name):
        user_input = input(f"Veuillez entrer la valeur pour {variable_name}: ")
        return user_input

    def save_to_env_file(self):
        print(self.env)
        with open(".env", "w") as env_file:
            for key in self.env:
                env_file.write(f"{key}={self.env[key]}\n")
    def setup_config(self):
        for envkey in self.env:
            if self.env[envkey]==None:
                self.env[envkey] = self.get_user_input(envkey)
if __name__ == "__main__":
    config = Config()
    config.setup_config()
    config.save_to_env_file()
