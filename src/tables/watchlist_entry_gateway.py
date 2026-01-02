import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class WatchlistEntryGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "watchlist_entries"
    
    def insert(self, user_id: int, anime_id: int, state: str, rating: int = None, progress: int = 0) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"""INSERT INTO {self.table_name} 
                    (user_id, anime_id, state, rating, progress) 
                    VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, anime_id, state, rating, progress))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    
    def select_by_id(self, user_id: int, anime_id: int) -> tuple:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {self.table_name} WHERE user_id = %s AND anime_id = %s"
        cursor.execute(query, (user_id, anime_id))
        row = cursor.fetchone()
        cursor.close()
        return row
