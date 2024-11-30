import os

import psycopg2

import config


class Database:
    def __init__(self):
        self.conn = Database.__create_conn()
        self.cursor = self.conn.cursor()

    @staticmethod
    def __create_conn():
        conn = psycopg2.connect(
            dbname=os.environ['DBNAME'],
            user=os.environ['DBUSER'],
            password=os.environ['DBPASS'],
            host=os.environ['DBHOST'],
            port=os.environ['DBPORT']
        )
        return conn

    def close(self):
        self.conn.close()
