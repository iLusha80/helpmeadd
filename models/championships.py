from database.connector import Database
from config import CHAMPIONSHIP_TABLE_NAME


class ChampionShipData:
    @staticmethod
    def insert(db: Database, name: str, url: str, season='2024-2025'):
        query = f"""INSERT INTO {CHAMPIONSHIP_TABLE_NAME} (name, url, season) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (url) DO NOTHING;"""

        db.cursor.execute(query, (name, url, season))
        db.conn.commit()
        print(f"Чемпионат '{name}' {season} успешно добавлен.")

    @staticmethod
    def select_all(db: Database):
        query = f"SELECT name, url, id, season FROM {CHAMPIONSHIP_TABLE_NAME}"
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        return result

    @staticmethod
    def select_current_season(db: Database, season: str = '2024-2025'):
        query = f"SELECT name, url, id, season FROM {CHAMPIONSHIP_TABLE_NAME} WHERE season = '{season}'"
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        return result
