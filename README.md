# AnimelistRDBMS

## About

This is a school project for managing anime watchlists. It is a web application built with Flask and MySQL that allows users to manage anime, genres, users, and watchlists.

## Libraries

- **Flask** - Web framework
- **mysql-connector-python** - MySQL database connector

## Features

- Anime management with genres
- User management
- Watchlist tracking with history
- CSV import functionality
- Database report generation

## Project Structure

```
AnimelistRDBMS/
├── src/
│   ├── config/
│   │   └── config.json
│   ├── frontend/
│   │   ├── static/
│   │   │   └── style.css
│   │   └── *.html
│   ├── routes/
│   │   ├── anime_routes.py
│   │   ├── genres_routes.py
│   │   ├── other_routes.py
│   │   ├── users_routes.py
│   │   └── watchlist_routes.py
│   ├── tables/
│   │   ├── anime_gateway.py
│   │   ├── anime_genre_gateway.py
│   │   ├── genre_gateway.py
│   │   ├── user_gateway.py
│   │   ├── watchlist_entry_gateway.py
│   │   └── watchlist_history_gateway.py
│   ├── connection.py
│   ├── database_setup.py
│   └── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```
git clone https://github.com/InkaEnFu/RDBMS-Project.git
cd AnimelistRDBMS
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure the application

Open `src/config/config.json` and set your database credentials:

```json
{
    "database": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "your_username",
        "password": "your_password",
        "database": "your_database_name"
    }
}
```

### 4. Generate the database setup script

Run the application for the first time:

```
cd src
python main.py
```

This will generate a customized SQL script file called `databaze.sql` in the project root directory based on your configuration values.

### 5. Execute the SQL script in MySQL Workbench

1. Open MySQL Workbench
2. Go to **File** > **Open SQL Script**
3. Select the generated `databaze.sql` file
4. Click the lightning bolt icon to execute the script

### 6. Run the application

```
cd src
python main.py
```

The application will be available at `http://localhost:5000`
