from typing import List, Dict

from database.connector import Database
from config import MATCH_DATA_TABLE_NAME


class MatchData:
    @staticmethod
    def insert_many(db: Database, data: List[Dict]) -> None:
        """
        Записываем данные о матчах в БД

        :param db: Экземпляр подключения к Базе Данных
        :type db: Database.Database
        :param data: Список словарей с данными о матчах
        :type data: List[Dict[str, Union[str, int]]]
        :return:
        """
        query = f"""INSERT INTO {MATCH_DATA_TABLE_NAME}
                    (matchtime, hometeam, awayteam, home_goals, away_goals, full_link, id_champ, match_fs_id, match_dt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (full_link) DO UPDATE 
                    SET id_champ = EXCLUDED.id_champ
                        ,match_fs_id = EXCLUDED.match_fs_id
                        ,match_dt = EXCLUDED.match_dt
                """
        values = list()
        for item in data:
            values.append((item['matchtime'], item['hometeam'], item['awayteam'], item['home_goals'],
                           item['away_goals'], item['full_link'], item['id_champ'], item['match_fs_id']))
        db.cursor.executemany(query, values)
        db.conn.commit()

    @staticmethod
    def get_random_unprocessed_matches(db: Database, count_matches: int = 1):
        query = f"""
        SELECT 
            id, full_link
        FROM {MATCH_DATA_TABLE_NAME}
        WHERE 1=1
            AND fl_detail = 0
            and match_dt < (now() - interval '3 hours')
        ORDER BY RANDOM()
        LIMIT {count_matches}
        """
        db.cursor.execute(query)
        return db.cursor.fetchall()

    @staticmethod
    def mark_match_as_processed(db: Database, match_id: int, fl_value: int = 1):
        query = f"""
        UPDATE {MATCH_DATA_TABLE_NAME}
        SET fl_detail = {fl_value}
        WHERE id = {match_id}
        """
        db.cursor.execute(query)
        db.conn.commit()

    @staticmethod
    def get_match_url_by_id(db: Database, match_id: int) -> str:
        query = f"""
        SELECT full_link
        FROM {MATCH_DATA_TABLE_NAME}
        WHERE id = {match_id}
        """
        db.cursor.execute(query)
        return db.cursor.fetchone()[0]