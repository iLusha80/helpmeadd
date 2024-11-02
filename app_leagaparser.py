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
        id_champ = row[2]
        saeson = row[3]
        url_result = f"{url}results/"
        print(f"Парсим данные из чемпионата '{name}'[{saeson}] с сайта {url}")
        ParserMatchInfo.get_match_info(driver=driver, db=db, url=url_result, id_champ=id_champ)
        print(f"Готово с чемпионатом '{name}'.")

    # Закрываем браузер
    driver.quit()


def get_archive_list(driver, url: str):
    url_archive = f"{url}archive/"
    driver.get(url_archive)
    css_selector_rows = '.archive__season .archive__text--clickable'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_rows)))
    rows = driver.find_elements(By.CSS_SELECTOR, css_selector_rows)
    for row in rows:
        link = row.get_attribute('href')
        season = row.text
        # print(f"Ссылка на архив сезона {season}: {link}")
        print(f"""csd.insert(db=db, name='{season}', url='{link}', season='{season.split()[-1]}')""")


if __name__ == "__main__":
    main()

