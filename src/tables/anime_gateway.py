import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class AnimeGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "anime"
    
    def insert(self, title_romaji: str, status: str, title_english: str = None, 
               episodes_total: int = 0, start_date: str = None, external_score: float = None) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"""INSERT INTO {self.table_name} 
                    (title_romaji, title_english, episodes_total, status, start_date, external_score) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (title_romaji, title_english, episodes_total, status, start_date, external_score))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    
    def select_by_id(self, id: int) -> tuple:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def update(self, id: int, title_romaji: str, status: str, title_english: str = None,
               episodes_total: int = 0, start_date: str = None, external_score: float = None) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"""UPDATE {self.table_name} 
                    SET title_romaji = %s, title_english = %s, episodes_total = %s, 
                        status = %s, start_date = %s, external_score = %s
                    WHERE id = %s"""
        cursor.execute(query, (title_romaji, title_english, episodes_total, status, start_date, external_score, id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def delete(self, id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
