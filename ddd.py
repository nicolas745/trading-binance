#!/bin/python3
import os

class Config:
    def __init__(self):
        self.testnet_api_secret = os.getenv("testnet_api_secret")
        self.testnet_api_key = os.getenv("testnet_api_key")
        self.api_secret = os.getenv("api_secret")
        self.api_key = os.getenv("api_key")

    def get_user_input(self, variable_name):
        user_input = input(f"Veuillez entrer la valeur pour {variable_name}: ")
        return user_input

    def save_to_env_file(self):
        with open(".env", "w") as env_file:
            env_file.write(f"testnet_api_secret={self.testnet_api_secret}\n")
            env_file.write(f"testnet_api_key={self.testnet_api_key}\n")
            env_file.write(f"api_secret={self.api_secret}\n")
            env_file.write(f"api_key={self.api_key}\n")

    def setup_config(self):
        if not self.testnet_api_secret:
            self.testnet_api_secret = self.get_user_input("testnet_api_secret")

        if not self.testnet_api_key:
            self.testnet_api_key = self.get_user_input("testnet_api_key")

        if not self.api_secret:
            self.api_secret = self.get_user_input("api_secret")

        if not self.api_key:
            self.api_key = self.get_user_input("api_key")

        self.save_to_env_file()

if __name__ == "__main__":
    config = Config()
    config.setup_config()
