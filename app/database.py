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
        """테이블 생성 및 컬럼 추가"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_analysis (
                id SERIAL PRIMARY KEY,
                image_path VARCHAR(255) NOT NULL,
                color VARCHAR(50),  -- 색상 컬럼
                shape VARCHAR(50),  -- 모양 컬럼
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def insert_result(self, image_path, color=None, shape=None):
        """새로운 분석 결과를 데이터베이스에 삽입"""
        self.cursor.execute("""
            INSERT INTO image_analysis (image_path, color, shape) 
            VALUES (%s, %s, %s) RETURNING id
        """, (image_path, color, shape))
        inserted_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return inserted_id

    def fetch_results(self):
        """저장된 결과에서 color와 shape만을 가져오는 함수"""
        self.cursor.execute("""
            SELECT 
                image_path,
                color,
                shape,
                analyzed_at
            FROM image_analysis
        """)
        return self.cursor.fetchall()

