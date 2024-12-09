import argparse
from concurrent.futures import ThreadPoolExecutor


from database.connector import Database
from driver.driver import Driver
from parsers.parser_match_time_line import ParserMatchTimeLine
from parsers.parser_match_statistics import ParserMatchStatistics

from models.match_data import MatchData
from logger import Logger

logger = Logger(__name__)


def get_data(driver, db: Database, current_step, total_steps, id_executor, match_id: int = None):

    if match_id:
        url = MatchData.get_match_url_by_id(db=db, match_id=match_id)
    else:
        match_id, url = MatchData.get_random_unprocessed_matches(db)[0]

    # logger.info(f"| {id_executor}ex | Матч: {match_id} | URL: {url}")

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

    MatchData.mark_match_as_processed(db=db, match_id=match_id, fl_value=2)

    txt = f"{id_executor}ex | Загруженно {current_step} из {total_steps} матчей ({(current_step / total_steps) * 100:.2f}%)"
    logger.info(txt)


def main(steps=1, id_executor=1, match_id: int = None):

    dcls = Driver(headers=True)
    driver = dcls.get_driver()
    db = Database()

    for current_step in range(1, steps + 1):
        get_data(driver=driver, db=db, current_step=current_step, total_steps=steps,
                 id_executor=id_executor, match_id=match_id)

    db.close()
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер данных с веб-сайта.")
    parser.add_argument('-s', '--steps', type=int, default=1,
                        help='Количество шагов (итераций) для выполнения на поток.')
    parser.add_argument('-p', '--pool', type=int, default=1, help='Количество потоков для выполнения.')
    parser.add_argument('-m', '--matches', type=int, help='Общее количество матчей для анализа.')
    parser.add_argument('-i', '--match_id', type=int, help='Идентификатор матча для загрузки.')
    args = parser.parse_args()
    if args.match_id:
        main(match_id=args.match_id)
    else:
        steps_per_executor = args.steps
        if args.matches:
            steps_per_executor = args.matches // args.pool

        with ThreadPoolExecutor(max_workers=args.pool) as executor:
            for i in range(args.pool):
                try:
                    executor.submit(main, steps=steps_per_executor, id_executor=i)
                except Exception as e:
                    logger.error(f"Ошибка при создании потока: {str(e)}")

    logger.warning("*ex | Все потоки завершены")
