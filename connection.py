
import mysql.connector


class DatabaseConnection:
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            self._connection = mysql.connector.connect(
                host="127.0.0.1",
                user="uzivatel",
                password="heslo",
                database="animelist"
            )
            print("Úspěšně připojeno k databázi.")
        return self._connection
    
    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


if __name__ == "__main__":
    db = DatabaseConnection()
    db.get_connection()
