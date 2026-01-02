from connection import DatabaseConnection
from menu import Menu


class Main:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.menu = None
    
    def start(self):
        print("=" * 50)
        print("       ANIMELIST - Starting application")
        print("=" * 50)
        
        try:
            self.db.get_connection()
            self.menu = Menu()
            self.menu.run()
        except Exception as e:
            print(f"✗ Error starting application: {e}")
        finally:
            self.db.close()
            print("Database connection closed.")


if __name__ == "__main__":
    app = Main()
    app.start()
