from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from database.connector import Database
from models.match_time_line import MatchTimeLineData
from utils.utils import Utils
from utils.web_utils import WebUtils
from logger import Logger

logger = Logger(__name__)

css_selectors = {
    'time_line_div' : '[class*="verticalSections"] > div',
    'half_title'    : 'div:first-child',
    'half_score'    : 'div:last-child',
    'incident'      : '[class$="incident"]',
    'timebox'       : '[class*="timeBox"]',
    'event_type'    : 'svg'

}


class ParserMatchTimeLine:
    @staticmethod
    @WebUtils.save_html_on_exit
    def get_match_time_line(driver: Chrome, match_id: int, db: Database, url: str):
        """

        :param driver:
        :param db:
        :param match_id:
        :param url:
        :return:
        """

        Utils.get_flashscore_url(driver=driver, url=url)

        result = Utils.load_page(driver=driver, css_selector=css_selectors['time_line_div'])

        if result != True:
            logger.error(f"Err - {result}\nurl - {url}")
            return False
        else:
            logger.debug(f"Success- {result}!\n Вот это дело! потекли данные")

        divs = driver.find_elements(By.CSS_SELECTOR, css_selectors['time_line_div'])

        for div in divs:
            css_class = div.get_attribute('class')
            if 'section__title' in css_class:
                half = div.find_element(By.CSS_SELECTOR, css_selectors['half_title']).text
                score = div.find_element(By.CSS_SELECTOR, css_selectors['half_score']).text
            else:
                if 'away' in css_class:
                    team = 2
                elif 'home' in css_class:
                    team = 1
                data = ParserMatchTimeLine.get_data_from_timeline_row(div=div)
                if data:
                    data['match_id'] = match_id
                    data['team_type'] = team
                    data['half'] = half

                    MatchTimeLineData.insert(db, **data)


    @staticmethod
    def get_data_from_timeline_row(div):
        data = dict()

        incedent = div.find_element(By.CSS_SELECTOR, css_selectors['incident'])

        # try:
        #     incedent = div.find_element(By.CSS_SELECTOR, css_selectors['incident'])
        # except:
        #     logger.error(f"Не найдено инцидента в css_selectors['incident']: {css_selectors['incident']}")
        #     return None

        timebox = incedent.find_element(By.CSS_SELECTOR, css_selectors['timebox']).text

        try:
            tmp = timebox.split("+")[0].replace("'", "")
            tmp = tmp.split(":")[0]
            data['minutes'] = int(tmp)
        except:
            data['minutes'] = -1
            logger.error(f"Не удалось распарсить время в css_selectors['timebox']: {css_selectors['timebox']}")

        try:
            data['add_minutes'] = int(timebox.split("+")[1].replace("'", ""))
        except:
            data['add_minutes'] = 0

        data['event_type'] = incedent.find_element(By.CSS_SELECTOR, css_selectors['event_type']).get_attribute('class')

        if not data['event_type']:
            data['event_type'] = '?gol?'

        data['player_name'] = incedent.find_elements(By.CSS_SELECTOR, 'a')[0].text

        if len(incedent.find_elements(By.CSS_SELECTOR, 'a')) > 1:
            data['assist_player_name'] = incedent.find_elements(By.CSS_SELECTOR, 'a')[1].text
        else:
            data['assist_player_name'] = 'Не указано'
        return data
