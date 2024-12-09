from database.connector import Database
from config import MATCH_TIME_LINE_TABLE_NAME


class MatchTimeLineData:
    @staticmethod
    def insert(db: Database, match_id: int, team_type: int, half: str, minutes: int, add_minutes: int,
               event_type: str, player_name: str, assist_player_name: str):

        query = f"""INSERT INTO {MATCH_TIME_LINE_TABLE_NAME}
                            (match_id, team_type, half, minutes, add_minutes, event_type, player_name, assist_player_name)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (match_id, team_type, half, minutes, add_minutes, event_type, player_name, assist_player_name)
        db.cursor.execute(query, values)
        db.conn.commit()

    @staticmethod
    def insert_many(db: Database, data: list[dict]):
        query = f"""INSERT INTO {MATCH_TIME_LINE_TABLE_NAME}
                    (match_id, team_type, half, minutes, add_minutes, event_type, player_name, assist_player_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = list()
        for item in data:
            values.append((item['match_id'], item['team_type'], item['half'],
                          item['minutes'], item['add_minutes'], item['event_type'],
                          item['player_name'], item['assist_player_name']))
        db.cursor.executemany(query, values)
        db.conn.commit()
