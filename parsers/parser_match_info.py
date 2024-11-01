from selenium.webdriver.common.by import By

from time import sleep

from database.connector import Database
from models.match_data import MatchData

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
    def get_match_info(driver, db: Database, url: str) -> list[dict]:

        driver.get(url)

        ParserMatchInfo.get_more_match(driver)

        matches = driver.find_elements(By.CSS_SELECTOR, css_selectors['matches'])
        print(f"Found {len(matches)} matches =)")

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

            result.append(dct)

        MatchData.insert_many(db, result)
        return result

    @staticmethod # .event__more--static
    def get_more_match(driver):
        sleep(5)  # Wait for page to load before clicking the button
        i = 0
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR, css_selectors['button_more'])
                button.click()
                i += 1
                print(f"Click - {i} time")
                sleep(5)  # Wait for page to load before clicking the button
                if i > 9:
                    return i
            except:
                print(f"Button not found: {i}")
                return i
