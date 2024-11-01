from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from database.connector import Database
from parsers.parser_match_info import ParserMatchInfo

from models.championships import ChampionShipData


def main():
    # Загружаем драйвер Chrome
    driver = webdriver.Chrome()
    db = Database()
    data = ChampionShipData.select_all(db=db)
    for row in data:
        name = row[0]
        url = row[1]
        url_result = f"{url}results/"
        print(f"Парсим данные из чемпионата '{name}' с сайта {url}")
        ParserMatchInfo.get_match_info(driver, db, url_result)
        print(f"Готово с чемпионатом '{name}'.")

    # Закрываем браузер
    driver.quit()


if __name__ == "__main__":
    main()

