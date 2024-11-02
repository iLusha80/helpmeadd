import os
from selenium import webdriver


class Driver:
    def __init__(self, headers: bool = True):
        self.options = webdriver.ChromeOptions()
        if headers:
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(options=self.options)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        # self.save_cookie()
        self.driver.quit()

    def __del__(self):
        self.close_driver()

    def save_cookie(self):
        cookies = self.driver.get_cookies()
        with open(os.path.join(os.getcwd(), 'cookies.txt'), 'w') as f:
            for cookie in cookies:
                f.write(f"{cookie['name']}={cookie['value']}\n")

    def load_cookie(self):
        with open(os.path.join(os.getcwd(), 'cookies.txt'), 'r') as f:
            cookies = [cookie.strip().split('=') for cookie in f.readlines()]
            for cookie in cookies:
                self.driver.add_cookie({'name': cookie[0], 'value': cookie[1]})


