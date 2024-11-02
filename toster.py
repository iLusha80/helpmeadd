from database.connector import Database
from models.match_data import MatchData
from models.championships import ChampionShipData as csd

db = Database()

csd.insert(db=db, name='Premier League', url='https://www.flashscorekz.com/football/england/premier-league/')
csd.insert(db=db, name='LaLiga', url='https://www.flashscorekz.com/football/spain/laliga/')
csd.insert(db=db, name='Bundesliga', url='https://www.flashscorekz.com/football/germany/bundesliga/')
csd.insert(db=db, name='Seria-A', url='https://www.flashscorekz.com/football/italy/serie-a/')
csd.insert(db=db, name='Ligue 1', url='https://www.flashscorekz.com/football/france/ligue-1/')
csd.insert(db=db, name='Champions League', url='https://www.flashscorekz.com/football/europe/champions-league/')
csd.insert(db=db, name='Euruopa League', url='https://www.flashscorekz.com/football/europe/europa-league/')
csd.insert(db=db, name='LaLiga2324', url='https://www.flashscorekz.com/football/spain/laliga-2023-2024/', season='2023-2024')

result = csd.select_all(db)
for row in result:
    print(row)
# #
# result = MatchData.get_random_unprocessed_match(db=db)
#
# #
# if result:
#     match_id, full_link = result
#     print(f"Processing match with ID: {match_id}, link: {full_link}")