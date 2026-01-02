import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class AnimeGenreGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "anime_genres"
    
    def insert(self, anime_id: int, genre_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO {self.table_name} (anime_id, genre_id) VALUES (%s, %s)"
        cursor.execute(query, (anime_id, genre_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    
    def select_by_id(self, anime_id: int, genre_id: int) -> tuple:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {self.table_name} WHERE anime_id = %s AND genre_id = %s"
        cursor.execute(query, (anime_id, genre_id))
        row = cursor.fetchone()
        cursor.close()
        return row
