from typing import Union, Dict

from database.connector import Database
from config import MATCH_STATISTICS_TABLE_NAME
from logger import Logger

logger = Logger(__name__)


class MatchStatisticsData:
    @staticmethod
    def insert(db: Database, match_id: int, team_type: int, half: str, indicator_name: str, value: Union[float, str]):

        query = f"""INSERT INTO {MATCH_STATISTICS_TABLE_NAME}
                                    (match_id, team_type, half, indicator_name, value)
                                    VALUES (%s, %s, %s, %s, %s)"""

        value = MatchStatisticsData.preprocess_value(value=value, indicator_name=indicator_name)
        if isinstance(value, dict):
            logger.info(value)
            for key, val in value.items():
                indicator_name = key
                value = val
                db.cursor.execute(query, (match_id, team_type, half, indicator_name, value))
                db.conn.commit()
        else:
            db.cursor.execute(query, (match_id, team_type, half, indicator_name, value))
            db.conn.commit()
            return

    @staticmethod
    def preprocess_value(value: Union[float, str], indicator_name: str) -> Union[float, str, Dict]:
        if isinstance(value, str) and '(' in value:
            values = dict()
            parts = value.split('(')[1].replace(')', '').split('/')
            values[f'{indicator_name} Успешных'] = int(parts[0])
            values[f'{indicator_name} Всего'] = int(parts[1])
            return values
        elif isinstance(value, str) and '%' in value:
            return float(value.replace('%', '')) / 100.0
        return value
