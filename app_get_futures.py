# Приложение для сбора расписания матчей по лигам

from driver.driver import Driver
from database.connector import Database
from parsers.parser_match_info import ParserMatchInfo
from models.championships import ChampionShipData


def main():
    """
    Основная точка входа
    """

    dcls = Driver(headers=False)
    driver = dcls.get_driver()
    db = Database()

    data = ChampionShipData.select_current_season(db=db)
    for row in data:
        name = row[0]
        url = row[1]
        id_champ = row[2]
        saeson = row[3]
        url_result = f"{url}fixtures/"
        print(f"Парсим данные из чемпионата '{name}'[{saeson}] с сайта {url}")
        ParserMatchInfo.get_match_info(driver=driver, db=db, url=url_result, id_champ=id_champ)
        print(f"Готово с чемпионатом '{name}'.")


if __name__ == '__main__':
    main()
