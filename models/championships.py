from database.connector import Database
from config import CHAMPIONSHIP_TABLE_NAME


class ChampionShipData:
    @staticmethod
    def insert(db: Database, name: str, url: str, season='2024-2025'):
        try:
            query = f"""INSERT INTO {CHAMPIONSHIP_TABLE_NAME} (name, url, season) 
            VALUES ('{name}', '{url}', '{season}') 
            ON CONFLICT (url) DO NOTHING;"""

            db.cursor.execute(query)
            db.conn.commit()
            print(f"Чемпионат '{name}' {season} успешно добавлен.")
        except db.cursor.IntegrityError:
            print(f"Запись с именем '{name}' уже существует, добавление пропущено.")

    @staticmethod
    def select_all(db: Database):
        query = f"SELECT name, url, id, season FROM {CHAMPIONSHIP_TABLE_NAME}"
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        return result
