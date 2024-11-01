#     match_id INTEGER NOT NULL,
#     team_type INTEGER NOT NULL,
#     half TEXT NOT NULL,
#     indicator_name TEXT NOT NULL,
#     value REAL,

from database.connector import Database
from config import MATCH_STATISTICS_TABLE_NAME


class MatchStatisticsData:
    @staticmethod
    def insert(db: Database, match_id: int, team_type: int, half: str, indicator_name: str, value: float):
        if isinstance(value, str) and '%' in value:
            value = float(value.replace('%', '')) / 100.0

        query = f"""INSERT INTO {MATCH_STATISTICS_TABLE_NAME}
                (match_id, team_type, half, indicator_name, value)
                VALUES ({match_id}, {team_type}, '{half}', '{indicator_name}', {value});"""

        db.cursor.execute(query)
        db.conn.commit()

    @staticmethod
    def insert_v2(db: Database, match_id: int, team_type: int, half: str, indicator_name: str, value: float):
        if isinstance(value, str) and '%' in value:
            value = float(value.replace('%', '')) / 100.0
        query = f"""INSERT INTO {MATCH_STATISTICS_TABLE_NAME}
                            (match_id, team_type, half, indicator_name, value)
                            VALUES (%s, %s, %s, %s, %s);"""
        db.cursor.execute(query, (match_id, team_type, half, indicator_name, value))
        db.conn.commit()

    @staticmethod
    def insert_many(db: Database, data: list[dict]):
        query = f"""INSERT INTO {MATCH_STATISTICS_TABLE_NAME}
                    (match_id, team_type, half, indicator_name, value)
                    VALUES (%s, %s, %s, %s, %s);"""
        values = list()
        for item in data:
            values.append((item['match_id'], item['team_type'], item['half'],
                          item['indicator_name'], item['value']))
        db.cursor.executemany(query, values)
        db.conn.commit()
