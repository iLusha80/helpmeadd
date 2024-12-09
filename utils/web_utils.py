from selenium.webdriver import Chrome


class WebUtils:
    @staticmethod
    def save_html_on_exit(func):
        def wrapper(driver: Chrome, *args, **kwargs):
            result = func(driver, *args, **kwargs)

            html = driver.page_source
            half = kwargs.get('half')
            match_id = kwargs.get('match_id')
            if half:
                file_name = f"statistic_{half}_{match_id}.html"
            else:
                file_name = f"time_line_{match_id}.html"

            WebUtils.save_html_to_file(html, file_name)
            return result
        return wrapper

    @staticmethod
    def get_random_prefix(length: int = 10) -> str:
        """
        Создает случайный префикс для имени файла

        :param length: Длина префикса (по умолчанию 10)
        :return: Случайный префикс
        """
        import random
        import string
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return prefix

    @staticmethod
    def save_html_to_file(html: str, file_path: str) -> None:
        """
        Сохраняет полученный html-код в указанный файл

        :param html: HTML-код
        :param file_path: Полное имя файла
        """
        file_path = 'data/htmls/' + file_path
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)
