from tables.anime_gateway import AnimeGateway
from tables.user_gateway import UserGateway
from tables.genre_gateway import GenreGateway
from tables.anime_genre_gateway import AnimeGenreGateway
from tables.watchlist_entry_gateway import WatchlistEntryGateway
from tables.watchlist_history_gateway import WatchlistHistoryGateway


class Menu:
    
    def __init__(self):
        self.anime_gw = AnimeGateway()
        self.user_gw = UserGateway()
        self.genre_gw = GenreGateway()
        self.anime_genre_gw = AnimeGenreGateway()
        self.watchlist_entry_gw = WatchlistEntryGateway()
        self.watchlist_history_gw = WatchlistHistoryGateway()
    
    def run(self):
        while True:
            self._show_main_menu()
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._anime_menu()
            elif choice == "2":
                self._user_menu()
            elif choice == "3":
                self._genre_menu()
            elif choice == "4":
                self._watchlist_entry_menu()
            elif choice == "5":
                self._watchlist_history_menu()
            elif choice == "0":
                print("Exiting application...")
                break
            else:
                print("Invalid choice, try again.")
    
    def _show_main_menu(self):
        print("\n" + "=" * 50)
        print("         ANIMELIST - MAIN MENU")
        print("=" * 50)
        print("1. Manage anime")
        print("2. Manage users")
        print("3. Manage genres")
        print("4. Manage watchlist entries")
        print("5. Manage watchlist history")
        print("0. Exit")
        print("=" * 50)
    
    def _anime_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE ANIME")
            print("-" * 40)
            print("1. Add new anime")
            print("2. Find anime by ID")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._anime_insert()
            elif choice == "2":
                self._anime_select_by_id()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _anime_insert(self):
        print("\n--- Add new anime ---")
        title_romaji = input("Title (romaji) *: ").strip()
        if not title_romaji:
            print("Title is required!")
            return
        
        title_english = input("Title (english, optional): ").strip() or None
        
        episodes_str = input("Episodes count (optional, default 0): ").strip()
        episodes_total = int(episodes_str) if episodes_str else 0
        
        status = input("Status (ONGOING/FINISHED/UPCOMING) *: ").strip().upper()
        if status not in ["ONGOING", "FINISHED", "UPCOMING"]:
            print("Invalid status!")
            return
        
        start_date = input("Start date (YYYY-MM-DD, optional): ").strip() or None
        
        score_str = input("External score (optional): ").strip()
        external_score = float(score_str) if score_str else None
        
        genres = self.genre_gw.select_all()
        selected_genre_ids = []
        if genres:
            print("\nAvailable genres:")
            for genre in genres:
                print(f"  {genre[0]}. {genre[1]}")
            print("\nEnter genre IDs separated by comma (e.g. 1,3,5) or leave empty:")
            genres_input = input("Genres: ").strip()
            if genres_input:
                try:
                    selected_genre_ids = [int(g.strip()) for g in genres_input.split(",")]
                except ValueError:
                    print("Invalid genre IDs, skipping genres.")
                    selected_genre_ids = []
        
        try:
            new_id = self.anime_gw.insert(title_romaji, status, title_english, 
                                          episodes_total, start_date, external_score)
            print(f"✓ Anime successfully added with ID: {new_id}")
            
            for genre_id in selected_genre_ids:
                try:
                    self.anime_genre_gw.insert(new_id, genre_id)
                    print(f"✓ Genre {genre_id} assigned")
                except Exception as e:
                    print(f"✗ Failed to assign genre {genre_id}: {e}")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _anime_select_by_id(self):
        print("\n--- Find anime ---")
        id_str = input("Enter anime ID: ").strip()
        
        try:
            anime_id = int(id_str)
            result = self.anime_gw.select_by_id(anime_id)
            if result:
                print(f"\nAnime found:")
                print(f"  ID: {result[0]}")
                print(f"  Title (romaji): {result[1]}")
                print(f"  Title (english): {result[2]}")
                print(f"  Episodes: {result[3]}")
                print(f"  Status: {result[4]}")
                print(f"  Start date: {result[5]}")
                print(f"  External score: {result[6]}")
            else:
                print("Anime with this ID was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _user_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE USERS")
            print("-" * 40)
            print("1. Add new user")
            print("2. Find user by ID")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._user_insert()
            elif choice == "2":
                self._user_select_by_id()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _user_insert(self):
        print("\n--- Add new user ---")
        username = input("Username *: ").strip()
        if not username:
            print("Username is required!")
            return
        
        email = input("E-mail *: ").strip()
        if not email:
            print("E-mail is required!")
            return
        
        is_admin_str = input("Is admin? (yes/no, default no): ").strip().lower()
        is_admin = is_admin_str in ["ano", "a", "yes", "y", "1", "true"]
        
        try:
            new_id = self.user_gw.insert(username, email, is_admin)
            print(f"✓ User successfully added with ID: {new_id}")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _user_select_by_id(self):
        print("\n--- Find user ---")
        id_str = input("Enter user ID: ").strip()
        
        try:
            user_id = int(id_str)
            result = self.user_gw.select_by_id(user_id)
            if result:
                print(f"\nUser found:")
                print(f"  ID: {result[0]}")
                print(f"  Username: {result[1]}")
                print(f"  E-mail: {result[2]}")
                print(f"  Is admin: {'Yes' if result[3] else 'No'}")
            else:
                print("User with this ID was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _genre_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE GENRES")
            print("-" * 40)
            print("1. Add new genre")
            print("2. Show all genres")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._genre_insert()
            elif choice == "2":
                self._genre_show_all()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _genre_insert(self):
        print("\n--- Add new genre ---")
        name = input("Genre name *: ").strip()
        if not name:
            print("Name is required!")
            return
        
        try:
            new_id = self.genre_gw.insert(name)
            print(f"✓ Genre successfully added with ID: {new_id}")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _genre_show_all(self):
        print("\n--- All genres ---")
        
        try:
            genres = self.genre_gw.select_all()
            if genres:
                print(f"\nFound {len(genres)} genres:")
                print("-" * 30)
                for genre in genres:
                    print(f"  {genre[0]}. {genre[1]}")
                print("-" * 30)
            else:
                print("No genres found.")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _watchlist_entry_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE WATCHLIST ENTRIES")
            print("-" * 40)
            print("1. Add entry to watchlist")
            print("2. Find entry")
            print("3. Show all watchlists")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._watchlist_entry_insert()
            elif choice == "2":
                self._watchlist_entry_select_by_id()
            elif choice == "3":
                self._watchlist_view()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _watchlist_entry_insert(self):
        print("\n--- Add entry to watchlist ---")
        
        try:
            user_id = int(input("User ID *: ").strip())
            anime_id = int(input("Anime ID *: ").strip())
            
            state = input("State (WATCHING/COMPLETED/PLAN_TO_WATCH/DROPPED/ON_HOLD) *: ").strip().upper()
            valid_states = ["WATCHING", "COMPLETED", "PLAN_TO_WATCH", "DROPPED", "ON_HOLD"]
            if state not in valid_states:
                print("Invalid state!")
                return
            
            rating_str = input("Rating 1-10 (optional): ").strip()
            rating = int(rating_str) if rating_str else None
            
            progress_str = input("Progress - episodes count (default 0): ").strip()
            progress = int(progress_str) if progress_str else 0
            
            success = self.watchlist_entry_gw.insert(user_id, anime_id, state, rating, progress)
            if success:
                print(f"✓ Entry successfully added to watchlist.")
            else:
                print("✗ Failed to add entry.")
        except ValueError:
            print("Invalid value!")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _watchlist_entry_select_by_id(self):
        print("\n--- Find watchlist entry ---")
        
        try:
            user_id = int(input("User ID: ").strip())
            anime_id = int(input("Anime ID: ").strip())
            
            result = self.watchlist_entry_gw.select_by_id(user_id, anime_id)
            if result:
                print(f"\nEntry found:")
                print(f"  User ID: {result[0]}")
                print(f"  Anime ID: {result[1]}")
                print(f"  State: {result[2]}")
                print(f"  Rating: {result[3]}")
                print(f"  Progress: {result[4]}")
            else:
                print("Entry was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _watchlist_view(self):
        print("\n--- All watchlists (view) ---")
        
        try:
            conn = self.watchlist_entry_gw.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_watchlist_view")
            results = cursor.fetchall()
            cursor.close()
            
            if results:
                print(f"\n{'User':<20} {'Anime':<30} {'Score':<10}")
                print("-" * 60)
                for row in results:
                    user_name = row[0] or "-"
                    anime_name = row[1] or "-"
                    score = row[2] if row[2] is not None else "-"
                    print(f"{user_name:<20} {anime_name:<30} {score:<10}")
                print("-" * 60)
            else:
                print("No watchlist entries found.")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _watchlist_history_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      WATCHLIST HISTORY")
            print("-" * 40)
            print("1. Find history by user ID")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._watchlist_history_select_by_user()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _watchlist_history_select_by_user(self):
        print("\n--- Find user history ---")
        id_str = input("Enter user ID: ").strip()
        
        try:
            user_id = int(id_str)
            results = self.watchlist_history_gw.select_by_user_id(user_id)
            if results:
                print(f"\nFound {len(results)} history entries for user {user_id}:")
                print("-" * 80)
                for result in results:
                    print(f"  History ID: {result[0]}")
                    print(f"  Anime ID: {result[2]}")
                    print(f"  Change date: {result[3]}")
                    print(f"  State: {result[4]} -> {result[5]}")
                    print(f"  Rating: {result[6]} -> {result[7]}")
                    print(f"  Progress: {result[8]} -> {result[9]}")
                    print("-" * 80)
            else:
                print("No history found for this user.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
