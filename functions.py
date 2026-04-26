import requests
import sqlite3
import json

url = "https://api.pokemontcg.io/v2/cards?q=name:pikachu"

def cards_by_name(name):
    params = {
        "q": f"name:{name}", # query of the parameter name 
        "pageSize": 250 #Request return size
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data["data"]