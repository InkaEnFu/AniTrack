import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class UserGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "users"
    
    def insert(self, username: str, email: str, is_admin: bool = False) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO {self.table_name} (username, email, is_admin) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, is_admin))
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
