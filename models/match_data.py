from database.connector import Database
from config import MATCH_DATA_TABLE_NAME


class MatchData:
    # @staticmethod
    # def insert(db: Database, matchtime: str, hometeam: str, awayteam: str,
    #                home_goals: int, away_goals: int, full_link: str):
    #     query = f"""INSERT INTO {MATCH_DATA_TABLE_NAME}
    #             (matchtime, hometeam, awayteam, home_goals, away_goals, full_link)
    #             VALUES ('{matchtime}', '{hometeam}', '{awayteam}', {home_goals}, {away_goals}, '{full_link}');"""
    #     db.cursor.execute(query)
    #     db.conn.commit()

    @staticmethod
    def insert_many(db: Database, data: list[dict]):
        query = f"""INSERT INTO {MATCH_DATA_TABLE_NAME}
                    (matchtime, hometeam, awayteam, home_goals, away_goals, full_link, id_champ)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (full_link) DO UPDATE SET id_champ = EXCLUDED.id_champ; """
        values = list()
        for item in data:
            values.append((item['matchtime'], item['hometeam'], item['awayteam'],
                          item['home_goals'], item['away_goals'], item['full_link'], item['id_champ']))
        db.cursor.executemany(query, values)
        db.conn.commit()

    @staticmethod
    def get_random_unprocessed_match(db: Database):
        query = f"""
        SELECT 
            id, full_link
        FROM {MATCH_DATA_TABLE_NAME}
        WHERE 1=1
            AND fl_detail = 0
        ORDER BY RANDOM()
        LIMIT 1;
        """
        db.cursor.execute(query)
        result = db.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None

    @staticmethod
    def mark_match_as_processed(db: Database, match_id: int, fl_value: int = 1):
        query = f"""
        UPDATE {MATCH_DATA_TABLE_NAME}
        SET fl_detail = {fl_value}
        WHERE id = {match_id};
        """
        db.cursor.execute(query)
        db.conn.commit()
