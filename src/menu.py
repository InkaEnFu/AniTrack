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
                self._anime_genre_menu()
            elif choice == "5":
                self._watchlist_entry_menu()
            elif choice == "6":
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
        print("4. Manage anime-genres")
        print("5. Manage watchlist entries")
        print("6. Manage watchlist history")
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
        
        try:
            new_id = self.anime_gw.insert(title_romaji, status, title_english, 
                                          episodes_total, start_date, external_score)
            print(f"✓ Anime successfully added with ID: {new_id}")
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
            print("2. Find genre by ID")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._genre_insert()
            elif choice == "2":
                self._genre_select_by_id()
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
    
    def _genre_select_by_id(self):
        print("\n--- Find genre ---")
        id_str = input("Enter genre ID: ").strip()
        
        try:
            genre_id = int(id_str)
            result = self.genre_gw.select_by_id(genre_id)
            if result:
                print(f"\nGenre found:")
                print(f"  ID: {result[0]}")
                print(f"  Name: {result[1]}")
            else:
                print("Genre with this ID was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _anime_genre_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE ANIME-GENRES")
            print("-" * 40)
            print("1. Assign genre to anime")
            print("2. Find link")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._anime_genre_insert()
            elif choice == "2":
                self._anime_genre_select_by_id()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _anime_genre_insert(self):
        print("\n--- Assign genre to anime ---")
        
        try:
            anime_id = int(input("Anime ID *: ").strip())
            genre_id = int(input("Genre ID *: ").strip())
            
            success = self.anime_genre_gw.insert(anime_id, genre_id)
            if success:
                print(f"✓ Genre successfully assigned to anime.")
            else:
                print("✗ Failed to assign genre.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _anime_genre_select_by_id(self):
        print("\n--- Find anime-genre link ---")
        
        try:
            anime_id = int(input("Anime ID: ").strip())
            genre_id = int(input("Genre ID: ").strip())
            
            result = self.anime_genre_gw.select_by_id(anime_id, genre_id)
            if result:
                print(f"\nLink found:")
                print(f"  Anime ID: {result[0]}")
                print(f"  Genre ID: {result[1]}")
            else:
                print("Link was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def _watchlist_entry_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE WATCHLIST ENTRIES")
            print("-" * 40)
            print("1. Add entry to watchlist")
            print("2. Find entry")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._watchlist_entry_insert()
            elif choice == "2":
                self._watchlist_entry_select_by_id()
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
    
    def _watchlist_history_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("      MANAGE WATCHLIST HISTORY")
            print("-" * 40)
            print("1. Add entry to history")
            print("2. Find entry by ID")
            print("0. Back")
            print("-" * 40)
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                self._watchlist_history_insert()
            elif choice == "2":
                self._watchlist_history_select_by_id()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def _watchlist_history_insert(self):
        print("\n--- Add entry to history ---")
        
        valid_states = ["WATCHING", "COMPLETED", "PLAN_TO_WATCH", "DROPPED", "ON_HOLD"]
        
        try:
            user_id = int(input("User ID *: ").strip())
            anime_id = int(input("Anime ID *: ").strip())
            
            old_state = input("Old state *: ").strip().upper()
            if old_state not in valid_states:
                print("Invalid old state!")
                return
            
            new_state = input("New state *: ").strip().upper()
            if new_state not in valid_states:
                print("Invalid new state!")
                return
            
            old_progress = int(input("Old progress *: ").strip())
            new_progress = int(input("New progress *: ").strip())
            
            old_rating_str = input("Old rating (optional): ").strip()
            old_rating = int(old_rating_str) if old_rating_str else None
            
            new_rating_str = input("New rating (optional): ").strip()
            new_rating = int(new_rating_str) if new_rating_str else None
            
            new_id = self.watchlist_history_gw.insert(
                user_id, anime_id, old_state, new_state,
                old_progress, new_progress, old_rating, new_rating
            )
            print(f"✓ History entry successfully added with ID: {new_id}")
        except ValueError:
            print("Invalid value!")
        except Exception as e:
            print(f"✗ Error adding: {e}")
    
    def _watchlist_history_select_by_id(self):
        print("\n--- Find history entry ---")
        id_str = input("Enter entry ID: ").strip()
        
        try:
            history_id = int(id_str)
            result = self.watchlist_history_gw.select_by_id(history_id)
            if result:
                print(f"\nEntry found:")
                print(f"  ID: {result[0]}")
                print(f"  User ID: {result[1]}")
                print(f"  Anime ID: {result[2]}")
                print(f"  Old state: {result[3]}")
                print(f"  New state: {result[4]}")
                print(f"  Old rating: {result[5]}")
                print(f"  New rating: {result[6]}")
                print(f"  Old progress: {result[7]}")
                print(f"  New progress: {result[8]}")
                print(f"  Change date: {result[9]}")
            else:
                print("Entry with this ID was not found.")
        except ValueError:
            print("Invalid ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
