import psycopg2
from datetime import datetime

class Database:
    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_analysis (
                id SERIAL PRIMARY KEY,
                image BYTEA NOT NULL,
                result TEXT NOT NULL,
                analyzed_at TIMESTAMP NOT NULL
            );
        """)
        self.connection.commit()

    def insert_analysis(self, image_data, result):
        query = """
            INSERT INTO image_analysis (image, result, analyzed_at)
            VALUES (%s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (image_data, result, datetime.now()))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def close(self):
        self.cursor.close()
        self.connection.close()
