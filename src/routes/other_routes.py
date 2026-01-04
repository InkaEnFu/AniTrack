from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv
import io
from connection import DatabaseConnection
from tables.anime_gateway import AnimeGateway
from tables.genre_gateway import GenreGateway

other_bp = Blueprint('other', __name__)

db = DatabaseConnection()
anime_gw = AnimeGateway()
genre_gw = GenreGateway()


@other_bp.route('/report')
def report():
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM anime")
    anime_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM genres")
    genre_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM watchlist_entries")
    watchlist_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT g.name, COUNT(ag.anime_id) as anime_count
        FROM genres g
        LEFT JOIN anime_genres ag ON g.id = ag.genre_id
        GROUP BY g.id, g.name
        ORDER BY anime_count DESC
    """)
    genres_stats = cursor.fetchall()
    
    cursor.close()
    
    return render_template('report.html', 
                           anime_count=anime_count,
                           user_count=user_count,
                           genre_count=genre_count,
                           watchlist_count=watchlist_count,
                           genres_stats=genres_stats)


@other_bp.route('/import', methods=['GET', 'POST'])
def import_csv():
    if request.method == 'POST':
        import_type = request.form.get('import_type')
        file = request.files.get('csv_file')
        
        if not file or file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('other.import_csv'))
        
        if not file.filename.endswith('.csv'):
            flash('File must be CSV format', 'error')
            return redirect(url_for('other.import_csv'))
        
        try:
            stream = io.StringIO(file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            count = 0
            
            if import_type == 'anime':
                for row in reader:
                    title_romaji = row.get('title_romaji', '')
                    title_english = row.get('title_english') or None
                    episodes = int(row.get('episodes_total', 0) or 0)
                    status = row.get('status', 'ONGOING')
                    start_date = row.get('start_date') or None
                    external_score = float(row.get('external_score')) if row.get('external_score') else None
                    
                    if title_romaji:
                        anime_gw.insert(title_romaji, status, title_english, episodes, start_date, external_score)
                        count += 1
                        
            elif import_type == 'genres':
                for row in reader:
                    name = row.get('name', '')
                    if name:
                        genre_gw.insert(name)
                        count += 1
            
            flash(f'Successfully imported {count} records', 'success')
            
        except Exception as e:
            flash(f'Import failed: {e}', 'error')
        
        return redirect(url_for('other.import_csv'))
    
    return render_template('import.html')
