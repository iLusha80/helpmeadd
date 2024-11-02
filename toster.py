from database.connector import Database
from models.match_data import MatchData
from models.championships import ChampionShipData as csd

db = Database()

suff = {
    # 'Premier League': 'https://www.flashscorekz.com/football/england/premier-league',
    'LaLiga': 'https://www.flashscorekz.com/football/spain/laliga',
    'Bundesliga': 'https://www.flashscorekz.com/football/germany/bundesliga',
    'Seria-A': 'https://www.flashscorekz.com/football/italy/serie-a',
    'Ligue 1': 'https://www.flashscorekz.com/football/france/ligue-1',
    'Champions League': 'https://www.flashscorekz.com/football/europe/champions-league',
    'Europa League': 'https://www.flashscorekz.com/football/europe/europa-league'
}
seasons = ['2023-2024', '2022-2023'] #, '2021-2022', '2020-2021']

# csd.insert(db=db, name='Premier League 2022-2023',
#            url='https://www.flashscorekz.com/football/england/premier-league-2022-2023/',
#            season='2022-2023')

# for key, url in suff.items():
#     for season in seasons:
#         name = f'{key} {season}'
#         tmp_url = f'{url}-{season}/'
#         print(name, tmp_url, season)
#         csd.insert(db=db, name=name, url=tmp_url, season=season)
        # print(f'{name} | {season} | {tmp_url}-{season}')


# # csd.insert(db=db, name='Premier League', url='https://www.flashscorekz.com/football/england/premier-league/')
# # csd.insert(db=db, name='LaLiga', url='https://www.flashscorekz.com/football/spain/laliga/')
# # csd.insert(db=db, name='Bundesliga', url='https://www.flashscorekz.com/football/germany/bundesliga/')
# # csd.insert(db=db, name='Seria-A', url='https://www.flashscorekz.com/football/italy/serie-a/')
# # csd.insert(db=db, name='Ligue 1', url='https://www.flashscorekz.com/football/france/ligue-1/')
# # csd.insert(db=db, name='Champions League', url='https://www.flashscorekz.com/football/europe/champions-league/')
# # csd.insert(db=db, name='Euruopa League', url='https://www.flashscorekz.com/football/europe/europa-league/')
# # csd.insert(db=db, name='LaLiga2324', url='https://www.flashscorekz.com/football/spain/laliga-2023-2024/', season='2023-2024')
# csd.insert(db=db, name='Премьер-лига 2023/2024', url='https://www.flashscorekz.com/football/england/premier-league-2023-2024/', season='2023/2024')
# csd.insert(db=db, name='Премьер-лига 2022/2023', url='https://www.flashscorekz.com/football/england/premier-league-2022-2023/', season='2022/2023')
# csd.insert(db=db, name='Премьер-лига 2021/2022', url='https://www.flashscorekz.com/football/england/premier-league-2021-2022/', season='2021/2022')
# csd.insert(db=db, name='Премьер-лига 2020/2021', url='https://www.flashscorekz.com/football/england/premier-league-2020-2021/', season='2020/2021')

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