
import mysql.connector
from mysql.connector import Error as MySQLError
import json
import os


class ConfigError(Exception):
    pass


class DatabaseError(Exception):
    pass


class Config:
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self):
        if self._config is None:
            config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
                print(f"Configuration loaded from {config_path}")
            except FileNotFoundError:
                print(f"Config file not found at {config_path}, using defaults.")
                self._config = {
                    "database": {
                        "host": "127.0.0.1",
                        "port": 3306,
                        "user": "uzivatel",
                        "password": "heslo",
                        "database": "animelist"
                    },
                    "app": {
                        "debug": True,
                        "port": 5000,
                        "secret_key": "animelist_secret_key"
                    }
                }
            except json.JSONDecodeError as e:
                raise ConfigError(f"Invalid JSON in config file: {e}")
        return self._config
    
    def get_database_config(self):
        return self.load().get("database", {})
    
    def get_app_config(self):
        return self.load().get("app", {})


class DatabaseConnection:
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                config = Config().get_database_config()
                self._connection = mysql.connector.connect(
                    host=config.get("host", "127.0.0.1"),
                    port=config.get("port", 3306),
                    user=config.get("user", "uzivatel"),
                    password=config.get("password", "heslo"),
                    database=config.get("database", "animelist"),
                    auth_plugin='mysql_native_password'
                )
                print("Successfully connected to database.")
            except MySQLError as e:
                error_messages = {
                    1045: "Access denied - wrong username or password",
                    1049: "Database does not exist",
                    2003: "Cannot connect to MySQL server - check if server is running",
                }
                msg = error_messages.get(e.errno, str(e))
                raise DatabaseError(f"Database connection failed: {msg}")
        return self._connection
    
    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


if __name__ == "__main__":
    db = DatabaseConnection()
    db.get_connection()
