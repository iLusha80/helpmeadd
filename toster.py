from database.connector import Database
from models.match_data import MatchData
from models.championships import ChampionShipData as csd

db = Database()

csd.insert(db=db, name='Premier League', url='https://www.flashscorekz.com/football/england/premier-league/')
csd.insert(db=db, name='LaLiga', url='https://www.flashscorekz.com/football/spain/laliga/')

result = csd.select_all(db)
for row in result:
    print(row)
#
result = MatchData.get_random_unprocessed_match(db=db)

#
if result:
    match_id, full_link = result
    print(f"Processing match with ID: {match_id}, link: {full_link}")