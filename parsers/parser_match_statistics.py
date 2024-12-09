from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome


from database.connector import Database
from models.match_statistics import MatchStatisticsData
from utils.utils import Utils
from utils.web_utils import WebUtils
from logger import Logger


css_selectors = {
    'statistics_rows'   : '[data-testid="wcl-statistics"]',
    'home_values'       : '[class*="homeValue"]',
    'away_values'       : '[class*="awayValue"]',
    'categories'        : 'div[class*="category"] > div[class*="category"]',
    'match_dt'          : '.duelParticipant__startTime'
}

logger = Logger(__name__)


class ParserMatchStatistics:
    @staticmethod
    @WebUtils.save_html_on_exit
    def get_match_statistics(driver: Chrome, db: Database, match_id: int, half: str, url: str):

        Utils.get_flashscore_url(driver=driver, url=url)
        result = Utils.load_page(driver=driver, css_selector=css_selectors['statistics_rows'])

        if result != True:
            logger.error(f"Err - {result}\nurl - {url}")
            return
        else:
            logger.debug(f"Success- {result}!\nurl - {url}")

        statistics_rows = driver.find_elements(By.CSS_SELECTOR, css_selectors['statistics_rows'])

        for i, row in enumerate(statistics_rows):
            try:
                home_data, away_data = ParserMatchStatistics.get_data_from_row(row, match_id, half)
                MatchStatisticsData.insert(db, **home_data)
                MatchStatisticsData.insert(db, **away_data)
            except Exception as e:
                logger.info(f"Ошибка получения данных из строчки статистики: {row.text}")
                logger.info(f"row - {i}")
                print("-" * 200)
                logger.info(f"Error: {str(e)}")
                print("-" * 200)
                continue


    @staticmethod
    def get_data_from_row(row, match_id, half):
        try:
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
        except Exception as e:
            logger.error(f"Ошибка получения данных из строчки статистики: {row.text}")
            logger.error(f"category - {category}, home_value - {home_value}, away_value - {away_value}")
            logger.error(f"Error: {str(e)}")
            raise ValueError(f"{str(e)}")

