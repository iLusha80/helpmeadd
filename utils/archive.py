from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OldUtils:
    @staticmethod
    def get_archive_list(driver: webdriver.Chrome, url: str) -> List[Tuple]:
        """
        Поиск ссылок на предыдущие сезоны
        :param driver: Драйвер
        :param url: Ссылка на чемпионат
        :return: Список найденных ссылок
        :rtype: List[Tuple]
        """
        url_archive = f"{url}archive/"
        driver.get(url_archive)
        css_selector_rows = '.archive__season .archive__text--clickable'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_rows)))
        rows = driver.find_elements(By.CSS_SELECTOR, css_selector_rows)
        result = list()
        for row in rows:
            link = row.get_attribute('href')
            season = row.text
            print(f"""csd.insert(db=db, name='{season}', url='{link}', season='{season.split()[-1]}')""")
            result.append((season, link))
        return result
