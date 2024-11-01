from database.connector import Database
from config import CHAMPIONSHIP_TABLE_NAME


class ChampionShipData:
    @staticmethod
    def insert(db: Database, name: str, url: str):
        try:
            query = f"""INSERT INTO {CHAMPIONSHIP_TABLE_NAME} (name, url) 
            VALUES ('{name}', '{url}') 
            ON CONFLICT (url) DO NOTHING;"""

            db.cursor.execute(query)
            db.conn.commit()
            print(f"Чемпионат '{name}' успешно добавлен.")
        except db.cursor.IntegrityError:
            print(f"Запись с именем '{name}' уже существует, добавление пропущено.")

    @staticmethod
    def select_all(db: Database):
        query = f"SELECT name, url FROM {CHAMPIONSHIP_TABLE_NAME}"
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        return result
