from time import perf_counter
from selenium.webdriver.common.by import By


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
        try:
            button = driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler') #
            button.click()
            return True
        except Exception as e:
            # print(f'Error: {str(e)}')
            return False
