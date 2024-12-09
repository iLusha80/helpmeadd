import argparse
from concurrent.futures import ThreadPoolExecutor


from database.connector import Database
from driver.driver import Driver
from parsers.parser_match_time_line import ParserMatchTimeLine
from parsers.parser_match_statistics import ParserMatchStatistics

from models.match_data import MatchData
from utils.utils import Utils
from logger import Logger

logger = Logger(__name__)


def get_data(driver, db: Database, current_step, total_steps, id_executor):

    match_id, url = MatchData.get_random_unprocessed_matches(db)[0]

    logger.info(f"| {id_executor}ex | Начинаем загрузку матча {match_id}\n url - ({url})")

    # Get TimeLine data
    ParserMatchTimeLine.get_match_time_line(driver=driver, db=db, match_id=match_id, url=url)

    MatchData.mark_match_as_processed(db=db, match_id=match_id, fl_value=1)

    # Get Statistics data
    halfs = {
        'full_time': f'{url}/match-statistics/0',
        'first_half': f'{url}/match-statistics/1',
        'second_half': f'{url}/match-statistics/2'
    }

    # logger.info(halfs)

    for half in halfs:
        ParserMatchStatistics.get_match_statistics(driver=driver, db=db, match_id=match_id, half=half, url=halfs[half])

    MatchData.mark_match_as_processed(db=db, match_id=match_id, fl_value=2)

    txt = f"| {id_executor}ex | Загруженно {current_step} из {total_steps} матчей ({(current_step / total_steps) * 100:.2f}%)"
    logger.info(txt)


@Utils.execution_time
def main(steps=1, id_executor=1):

    dcls = Driver(headers=True)
    driver = dcls.get_driver()
    db = Database()

    for current_step in range(1, steps + 1):
        get_data(driver=driver, db=db, current_step=current_step, total_steps=steps, id_executor=id_executor)

    logger.info(f"Execuror - {id_executor} - Done!")

    db.close()
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер данных с веб-сайта.")
    parser.add_argument('-s', '--steps', type=int, default=1,
                        help='Количество шагов (итераций) для выполнения на поток.')
    parser.add_argument('-p', '--pool', type=int, default=1, help='Количество потоков для выполнения.')
    parser.add_argument('-m', '--matches', type=int, help='Общее количество матчей для анализа.')
    args = parser.parse_args()

    steps_per_executor = args.steps
    if args.matches:
        steps_per_executor = args.matches // args.pool

    with ThreadPoolExecutor(max_workers=args.pool) as executor:
        for i in range(args.pool):
            try:
                executor.submit(main, steps=steps_per_executor, id_executor=i)
            except Exception as e:
                logger.error(f"Ошибка при создании потока: {str(e)}")

    logger.warning("Все потоки завершены")
