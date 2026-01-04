import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import DatabaseConnection


class GenreGateway:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.table_name = "genres"
    
    def insert(self, name: str) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO {self.table_name} (name) VALUES (%s)"
        cursor.execute(query, (name,))
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
    
    def select_all(self) -> list:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY id")
        rows = cursor.fetchall()
        cursor.close()
        return rows
