from selenium import webdriver
import argparse

from database.connector import Database
from parsers.parser_match_time_line import ParserMatchTimeLine
from parsers.parser_match_statistics import ParserMatchStatistics

from models.match_data import MatchData


def get_data(driver, db: Database):
    match_id, url = MatchData.get_random_unprocessed_match(db)

    # Get TimeLine data
    ParserMatchTimeLine.get_match_time_line(driver=driver, db=db, match_id=match_id, url=url)

    MatchData.mark_match_as_processed(db=db, match_id=match_id, fl_value=1)

    # Get Statistics data
    halfs = {
        'full_time': f'{url}/match-statistics/0',
        'first_half': f'{url}/match-statistics/1',
        'second_half': f'{url}/match-statistics/2'
    }

    for half in halfs:
        ParserMatchStatistics.get_match_statistics(driver=driver, db=db, match_id=match_id, half=half, url=halfs[half])
        print(f"Half {half}, match_id={match_id} added")
    print(f"{'='*40} {url} | {match_id} {'='*40}")

    MatchData.mark_match_as_processed(db=db, match_id=match_id, fl_value=2)


def main(steps=1):

    driver = webdriver.Chrome()
    db = Database()

    for _ in range(steps):
        get_data(driver=driver, db=db)

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер данных с веб-сайта.")
    parser.add_argument('-s', '--steps', type=int, default=1, help='Количество шагов (итераций) для выполнения.')
    args = parser.parse_args()
    main(steps=args.steps)
