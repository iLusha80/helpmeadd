from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from database.connector import Database
from models.match_statistics import MatchStatisticsData
from utils.utils import Utils
from logger import Logger


css_selectors = {
    'statistics_rows'   : '[data-testid="wcl-statistics"]',
    'home_values'       : '[class*="homeValue"]',
    'away_values'       : '[class*="awayValue"]',
    'categories'        : 'div[class*="category"] > div[class*="category"]'
}

logger = Logger(__name__)


class ParserMatchStatistics:
    @staticmethod
    def get_match_statistics(driver, db: Database, match_id: int, half: str, url: str):

        Utils.get_flashscore_url(driver=driver, url=url)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selectors['statistics_rows']))
            )
            statistics_rows = driver.find_elements(By.CSS_SELECTOR, css_selectors['statistics_rows'])
            logger.info(f"Найдено {len(statistics_rows)} строк статистики")
        except:
            logger.error(f"Не найдены строки css_selector: {css_selectors['statistics_rows']}")
            return False

        # statistics_rows = driver.find_elements(By.CSS_SELECTOR, css_selectors['statistics_rows'])

        for row in statistics_rows:
            home_data, away_data = ParserMatchStatistics.get_data_from_row(row, match_id, half)
            # try:
            #     home_data, away_data = ParserMatchStatistics.get_data_from_row(row, match_id, half)
            # except Exception as e:
            #     logger.error(f"Ошибка при получении данных из строки: {str(e)}")
            #     break

            logger.debug(f"Home_data: {home_data}")
            logger.debug(f"Away_data: {away_data}")
            MatchStatisticsData.insert(db, **home_data)
            MatchStatisticsData.insert(db, **away_data)

    @staticmethod
    def get_data_from_row(row, match_id, half):
        home_data = dict()
        away_data = dict()

        category = row.find_element(By.CSS_SELECTOR, css_selectors['categories']).text
        home_value = row.find_element(By.CSS_SELECTOR, css_selectors['home_values']).text
        away_value = row.find_element(By.CSS_SELECTOR, css_selectors['away_values']).text
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

        return home_data, away_data

