import requests
import sqlite3
import json
import time

url = "https://api.pokemontcg.io/v2/cards?q=name:pikachu"


def cards_by_name(name):
    params = {
        "q": f"name:{name}", # query of the parameter name 
        "pageSize": 250 #Request return size
    }

    cards_main = requests.get(url, params=params)
    if (cards_main.status_code == 200):
        main_data = cards_main.json().get("data", [])
        if not main_data:
            print("No cards found:", name)
        else:
            print("API SUCEED:", name)
    else:
        print("API failed:", cards_main.status_code)
        print("Fail:", name)
        return
    
    
    return {
            "data": main_data
        }

def parse_card(card):
    prices = card.get("tcgplayer", {}).get("prices",{})

    results = []

    for variant, data in prices.items():
        results.append({
            "id": card.get("id"),
            "name": card.get("name"),
            "set": card.get("set", {}).get("name"),
            "variant": variant,
            "market_price": data.get("market")
            })
        
    return results
    
def insert_cards(cursor, card):
    cursor.execute("""
        INSERT INTO cards (id,name, set_name, variant, market_price)
        VALUES (?, ?, ?, ?, ?)
    """, (
        card["id"],
        card["name"],
        card["set"],
        card["variant"],
        card["market_price"]
    ))


def update_desired(cursor):
    with open("desired.txt", "r") as f:
        content = f.read().splitlines()
    for name in content:
        out = cards_by_name(name)
        time.sleep(0.1)  # 100ms between calls
        #print(type(out)) #DEBUG
        for cards in out["data"]:
            temp = parse_card(cards)
            for c in temp:
                #print(type(c),c) # DEBUG
                insert_cards(cursor, c)


