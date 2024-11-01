from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from database.connector import Database
from models.match_statistics import MatchStatisticsData
from utils.utils import Utils


css_selectors = {
    'statistics_rows'   : '[data-testid="wcl-statistics"]',
    'home_values'       : '[class*="homeValue"]',
    'away_values'       : '[class*="awayValue"]',
    'categories'        : 'div[class*="category"] > div[class*="category"]'
}


class ParserMatchStatistics:
    @staticmethod
    def get_match_statistics(driver, db: Database, match_id: int, half: str, url: str):
        Utils.get_flashscore_url(driver=driver, url=url)

        try:
            # Ожидание появления элемента в течение 3 секунд
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selectors['statistics_rows']))
            )
            statistics_rows = driver.find_elements(By.CSS_SELECTOR, css_selectors['statistics_rows'])
        except:
            # Если элемент не появился за 3 секунд, выполнится этот блок
            print("Элемент не найден за отведенное время")
            return False

        home_data = dict()
        away_data = dict()

        # statistics_rows = driver.find_elements(By.CSS_SELECTOR, css_selectors['statistics_rows'])
        print(f"len statistics_rows - {len(statistics_rows)}")

        for row in statistics_rows:
            category = row.find_element(By.CSS_SELECTOR, css_selectors['categories']).text
            home_value = row.find_element(By.CSS_SELECTOR, css_selectors['home_values']).text
            away_value = row.find_element(By.CSS_SELECTOR, css_selectors['away_values']).text
            # ['match_id', 'team_type', 'half', 'indicator_name', 'value']
            home_data['match_id'] = match_id
            away_data['match_id'] = match_id
            home_data['team_type'] = 1
            away_data['team_type'] = 2
            home_data['half'] = half
            away_data['half'] = half
            home_data['indicator_name'] = category
            away_data['indicator_name'] = category
            home_data['value'] = home_value
            away_data['value'] = away_value

            MatchStatisticsData.insert_v2(db, **home_data)
            MatchStatisticsData.insert_v2(db, **away_data)
