import requests
import sqlite3
import json
from functions import cards_by_name

#print("Imports successful")

# --- API TEST ---
url = "https://api.pokemontcg.io/v2/cards?q=name:pikachu"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    card = data["data"][0]
    print("API working:", card["name"])
    #print(json.dumps(data["data"][0], indent=2))
else:
    print("API failed:", response.status_code)

# --- DATABASE TEST ---
conn = sqlite3.connect("test_cards.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY,
    name TEXT
)
""")

cursor.execute(
    "INSERT OR IGNORE INTO cards VALUES (?, ?)",
    (card["id"], card["name"])
)

conn.commit()

cursor.execute("SELECT * FROM cards")
rows = cursor.fetchall()

print("DB working, rows:", rows)

conn.close()

#print(json.dumps(cards_by_name("Nihilego"), indent=2))
data = cards_by_name("Nihilego")
with open("output.json", "w") as f: #w is overwrie, a is append to file
    json.dump(data, f, indent=4)

