import requests
import sqlite3
import json
from functions import update_desired


# --- API TEST ---
url = "https://api.pokemontcg.io/v2/cards?q=name:pikachu"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    card = data["data"][0]
    print("API working:", response.status_code)
    #print(json.dumps(data["data"][0], indent=2))
else:
    print("API failed:", response.status_code)

# --- DATABASE TEST ---
conn = sqlite3.connect("cards.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id TEXT,
    name TEXT,
    set_name TEXT,
    variant TEXT,           
    market_price REAL
)
""")

##
## Calls the TCGPLAYER API for all pokemon in desired.txt
## Adds each to the SQLite DB
## Type SQL Queries below, tehn do cursor.fetchall() to list the changes!
##
update_desired(cursor) 
conn.commit() #Persists all changes you have made

#Print Entire DB

# cursor.execute("SELECT * FROM cards") 
# rows = cursor.fetchall() #Retrieves all remaining rows  from the result of the last SELECT query
# print("DB working, rows:", rows)

#Delete any duplicates based on ID

cursor.execute("""
DELETE FROM cards
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM cards
    GROUP BY id
);
""")

#Print Top 10 Most Expensive

cursor.execute("""
SELECT name, set_name, variant, market_price
FROM cards
ORDER BY market_price DESC
LIMIT 10
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()#closes connection to db
