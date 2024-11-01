from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from database.connector import Database
from models.match_time_line import MatchTimeLineData
from utils.utils import Utils


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
    def get_match_time_line(driver, db: Database, match_id: int, url: str):
        """

        :param driver:
        :param db:
        :param match_id:
        :param url:
        :return:
        """

        Utils.get_flashscore_url(driver=driver, url=url)


        try:
            # Ожидание появления элемента в течение 3 секунд
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selectors['time_line_div']))
            )
            divs = driver.find_elements(By.CSS_SELECTOR, css_selectors['time_line_div'])
        except:
            # Если элемент не появился за 3 секунд, выполнится этот блок
            print("Элемент не найден за отведенное время")
            return False

        print(f"Количество дивов во временной линии: {len(divs)}")

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
                data = ParserMatchTimeLine.get_data_from_timeline_row(div=div, url=url)
                if data:
                    data['match_id'] = match_id
                    data['team_type'] = team
                    data['half'] = half

                    MatchTimeLineData.insert_v2(db, **data)


    @staticmethod
    def get_data_from_timeline_row(div, url):
        data = dict()
        try:
            incedent = div.find_element(By.CSS_SELECTOR, css_selectors['incident'])
        except:
            # input(f"Похоже пустой тайм ======== {url} =========")
            return None

        timebox = incedent.find_element(By.CSS_SELECTOR, css_selectors['timebox']).text
        data['minutes'] = int(timebox.split("+")[0].replace("'", ""))

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