# PokemonDatabase
Calls the TCGPLAYER API for all pokemon in desired.txt
Adds each to the SQLite DB
Type SQL Queries below, tehn do cursor.fetchall() to list the changes!

Current Issues:
*  TCGPLAYER API has no way to differentiate WorldChamionShip Deck cards or STAFF prerelease cards, they are not called into the db

Future Additions:
*  Add a cache to reduce calls to the API, especially for large sets of pokemon or popular pokemon


