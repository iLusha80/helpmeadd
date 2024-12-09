from time import perf_counter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Utils:
    @staticmethod
    def execution_time(func):
        def wrapper(*args, **kwargs):
            start_time = perf_counter()
            result = func(*args, **kwargs)
            end_time = perf_counter()
            execution_time = end_time - start_time
            print(f'Execution time of {func.__name__}: {execution_time:.2f} seconds')
            print(f'Args: {args}')
            print(f'kwargs: {kwargs}')
            return result
        return wrapper

    @staticmethod
    def get_flashscore_url(driver, url: str):
        driver.get(url)
        # button = driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler')  #
        # button.click()

        # try:
        #     button = driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler') #
        #     button.click()
        #     return True
        # except Exception as e:
        #     # print(f'Error: {str(e)}')
        #     return False

    @staticmethod
    def load_page(driver, css_selector: str):
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        try:
            # Ожидание появления элемента в течение 3 секунд
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return True
        except Exception as e:
            return str(e)

    @staticmethod
    def get_match_id_from_url(url: str) -> str:
        """
        Получаем ID матча из URL

        :param url: Ссылка на матч
        :return: ID матча
        :rtype: str
        """
        try:
            return url.split("/match/")[1].split("/")[0]
        except IndexError:
            raise ValueError("Invalid URL format.")

