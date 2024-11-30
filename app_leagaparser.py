from selenium import webdriver

from database.connector import Database
from parsers.parser_match_info import ParserMatchInfo

from models.championships import ChampionShipData


def main():
    """
    Основная точка входа
    """
    # Загружаем драйвер Chrome
    driver = webdriver.Chrome()
    db = Database()
    data = ChampionShipData.select_all(db=db)
    for row in data:
        name = row[0]
        url = row[1]
        id_champ = row[2]
        saeson = row[3]
        url_result = f"{url}results/"
        print(f"Парсим данные из чемпионата '{name}'[{saeson}] с сайта {url}")
        ParserMatchInfo.get_match_info(driver=driver, db=db, url=url_result, id_champ=id_champ)
        print(f"Готово с чемпионатом '{name}'.")

    # Закрываем браузер
    driver.quit()


if __name__ == "__main__":
    main()
