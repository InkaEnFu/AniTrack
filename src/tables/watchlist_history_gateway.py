import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class WatchlistHistoryGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "watchlist_history"
    
    def insert(self, user_id: int, anime_id: int, old_state: str, new_state: str,
               old_progress: int, new_progress: int, old_rating: int = None, new_rating: int = None) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"""INSERT INTO {self.table_name} 
                    (user_id, anime_id, old_state, new_state, old_rating, new_rating, old_progress, new_progress) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, anime_id, old_state, new_state, old_rating, new_rating, old_progress, new_progress))
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
