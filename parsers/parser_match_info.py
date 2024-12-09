from selenium.webdriver.common.by import By

from time import sleep
from typing import List, Dict

from database.connector import Database
from models.match_data import MatchData
from utils.utils import Utils
from logger import Logger

logger = Logger(__name__)


css_selectors = {
    'matches'           : '.event__match',
    'match_time'        : '.event__time',
    'match_time_alter'  : '.event__stage',
    'home_team'         : '.event__homeParticipant',
    'away_team'         : '.event__awayParticipant',
    'home_goals'        : '.event__score--home',
    'away_goals'        : '.event__score--away',
    'full_link'         : '.eventRowLink',
    'button_more'       : '.event__more--static'
    }


class ParserMatchInfo:
    @staticmethod
    def get_match_info(driver, db: Database, url: str, id_champ: int) -> List[Dict]:
        """
        Забираем информацию о матче из списка результатов

        :param driver:   Драйвер/Браузер
        :type driver:    Selenium.WebDriver.Chrome
        :param db:       Экземпляр подключения к Базе Данных
        :type db:        Database.Database
        :param url:      Ссылка на Лигу
        :param id_champ: ИД Чемпионата в базе
        :type id_champ:  int
        :return:
        """

        Utils.get_flashscore_url(driver=driver, url=url)

        ParserMatchInfo.get_more_match(driver)

        matches = driver.find_elements(By.CSS_SELECTOR, css_selectors['matches'])
        logger.info(f"Found {len(matches)} matches =)")

        result = list()

        for match in matches:
            dct = dict()
            try:
                dct['matchtime'] = match.find_element(By.CSS_SELECTOR, css_selectors['match_time']).text
            except:
                dct['matchtime'] = match.find_element(By.CSS_SELECTOR, css_selectors['match_time_alter']).text
            dct['hometeam'] = match.find_element(By.CSS_SELECTOR, css_selectors['home_team']).text
            dct['awayteam'] = match.find_element(By.CSS_SELECTOR, css_selectors['away_team']).text
            dct['home_goals'] = match.find_element(By.CSS_SELECTOR, css_selectors['home_goals']).text
            dct['away_goals'] = match.find_element(By.CSS_SELECTOR, css_selectors['away_goals']).text
            dct['full_link'] = match.find_element(By.CSS_SELECTOR, css_selectors['full_link']).get_attribute('href')
            dct['id_champ'] = id_champ
            dct['match_fs_id'] = Utils.get_match_id_from_url(dct['full_link'])

            result.append(dct)

        MatchData.insert_many(db, result)
        return result

    @staticmethod
    def get_more_match(driver):
        sleep(5)
        i = 0
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR, css_selectors['button_more'])
                button.click()
                i += 1
                sleep(5)
                if i > 9:
                    return i
            except:
                return i
