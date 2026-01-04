from flask import Flask, render_template, request, redirect, url_for, flash
from connection import DatabaseConnection
from tables.anime_gateway import AnimeGateway
from tables.user_gateway import UserGateway
from tables.genre_gateway import GenreGateway
from tables.anime_genre_gateway import AnimeGenreGateway
from tables.watchlist_entry_gateway import WatchlistEntryGateway
from tables.watchlist_history_gateway import WatchlistHistoryGateway

app = Flask(__name__, template_folder='frontend')
app.secret_key = 'animelist_secret_key'

db = DatabaseConnection()
anime_gw = AnimeGateway()
user_gw = UserGateway()
genre_gw = GenreGateway()
anime_genre_gw = AnimeGenreGateway()
watchlist_entry_gw = WatchlistEntryGateway()
watchlist_history_gw = WatchlistHistoryGateway()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/anime')
def anime_list():
    conn = db.get_connection()
    cursor = conn.cursor()
    search_id = request.args.get('id')
    if search_id:
        cursor.execute("SELECT * FROM anime_with_genres_view WHERE anime_id = %s", (search_id,))
    else:
        cursor.execute("SELECT * FROM anime_with_genres_view")
    anime = cursor.fetchall()
    cursor.close()
    return render_template('anime.html', anime=anime, search_id=search_id)


@app.route('/anime/add', methods=['GET', 'POST'])
def anime_add():
    if request.method == 'POST':
        title_romaji = request.form['title_romaji']
        title_english = request.form.get('title_english') or None
        episodes = int(request.form.get('episodes') or 0)
        status = request.form['status']
        start_date = request.form.get('start_date') or None
        external_score = float(request.form['external_score']) if request.form.get('external_score') else None
        genre_ids = request.form.getlist('genres')
        
        try:
            new_id = anime_gw.insert(title_romaji, status, title_english, episodes, start_date, external_score)
            for genre_id in genre_ids:
                anime_genre_gw.insert(new_id, int(genre_id))
            flash(f'Anime added successfully with ID: {new_id}', 'success')
            return redirect(url_for('anime_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    genres = genre_gw.select_all()
    return render_template('anime_add.html', genres=genres)


@app.route('/anime/edit/<int:id>', methods=['GET', 'POST'])
def anime_edit(id):
    if request.method == 'POST':
        title_romaji = request.form['title_romaji']
        title_english = request.form.get('title_english') or None
        episodes = int(request.form.get('episodes') or 0)
        status = request.form['status']
        start_date = request.form.get('start_date') or None
        external_score = float(request.form['external_score']) if request.form.get('external_score') else None
        
        try:
            anime_gw.update(id, title_romaji, status, title_english, episodes, start_date, external_score)
            flash('Anime updated successfully', 'success')
            return redirect(url_for('anime_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    anime = anime_gw.select_by_id(id)
    return render_template('anime_edit.html', anime=anime)


@app.route('/anime/delete/<int:id>')
def anime_delete(id):
    try:
        anime_gw.delete(id)
        flash('Anime deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('anime_list'))


@app.route('/users')
def user_list():
    conn = db.get_connection()
    cursor = conn.cursor()
    search_id = request.args.get('id')
    search_name = request.args.get('name')
    search_email = request.args.get('email')
    
    if search_id:
        cursor.execute("SELECT * FROM users WHERE id = %s", (search_id,))
    elif search_name:
        cursor.execute("SELECT * FROM users WHERE username LIKE %s", (f'%{search_name}%',))
    elif search_email:
        cursor.execute("SELECT * FROM users WHERE email LIKE %s", (f'%{search_email}%',))
    else:
        cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users, search_id=search_id, search_name=search_name, search_email=search_email)


@app.route('/users/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        is_admin = 'is_admin' in request.form
        
        try:
            new_id = user_gw.insert(username, email, is_admin)
            flash(f'User added successfully with ID: {new_id}', 'success')
            return redirect(url_for('user_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    return render_template('user_add.html')


@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        is_admin = 'is_admin' in request.form
        
        try:
            user_gw.update(id, username, email, is_admin)
            flash('User updated successfully', 'success')
            return redirect(url_for('user_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    user = user_gw.select_by_id(id)
    return render_template('user_edit.html', user=user)


@app.route('/users/delete/<int:id>')
def user_delete(id):
    try:
        user_gw.delete(id)
        flash('User deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('user_list'))


@app.route('/genres')
def genre_list():
    genres = genre_gw.select_all()
    return render_template('genres.html', genres=genres)


@app.route('/genres/add', methods=['GET', 'POST'])
def genre_add():
    if request.method == 'POST':
        name = request.form['name']
        
        try:
            new_id = genre_gw.insert(name)
            flash(f'Genre added successfully with ID: {new_id}', 'success')
            return redirect(url_for('genre_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    return render_template('genre_add.html')


@app.route('/genres/edit/<int:id>', methods=['GET', 'POST'])
def genre_edit(id):
    if request.method == 'POST':
        name = request.form['name']
        
        try:
            genre_gw.update(id, name)
            flash('Genre updated successfully', 'success')
            return redirect(url_for('genre_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    genre = genre_gw.select_by_id(id)
    return render_template('genre_edit.html', genre=genre)


@app.route('/genres/delete/<int:id>')
def genre_delete(id):
    try:
        genre_gw.delete(id)
        flash('Genre deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('genre_list'))


@app.route('/watchlist')
def watchlist():
    conn = db.get_connection()
    cursor = conn.cursor()
    search_user = request.args.get('user')
    search_anime = request.args.get('anime')
    
    if search_user:
        cursor.execute("SELECT * FROM user_watchlist_view WHERE user_name LIKE %s", (f'%{search_user}%',))
    elif search_anime:
        cursor.execute("SELECT * FROM user_watchlist_view WHERE anime_name LIKE %s", (f'%{search_anime}%',))
    else:
        cursor.execute("SELECT * FROM user_watchlist_view")
    entries = cursor.fetchall()
    cursor.close()
    return render_template('watchlist.html', entries=entries, search_user=search_user, search_anime=search_anime)


@app.route('/watchlist/add', methods=['GET', 'POST'])
def watchlist_add():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        anime_id = int(request.form['anime_id'])
        status = request.form['status']
        score = int(request.form['score']) if request.form.get('score') else None
        progress = int(request.form.get('progress') or 0)
        
        try:
            watchlist_entry_gw.insert(user_id, anime_id, status, score, progress)
            flash('Watchlist entry added successfully', 'success')
            return redirect(url_for('watchlist'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title_romaji FROM anime")
    anime = cursor.fetchall()
    cursor.close()
    return render_template('watchlist_add.html', users=users, anime=anime)


@app.route('/watchlist/edit/<int:user_id>/<int:anime_id>', methods=['GET', 'POST'])
def watchlist_edit(user_id, anime_id):
    if request.method == 'POST':
        status = request.form['status']
        score = int(request.form['score']) if request.form.get('score') else None
        progress = int(request.form.get('progress') or 0)
        
        try:
            watchlist_entry_gw.update(user_id, anime_id, status, score, progress)
            flash('Watchlist entry updated successfully', 'success')
            return redirect(url_for('watchlist'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    entry = watchlist_entry_gw.select_by_id(user_id, anime_id)
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.execute("SELECT title_romaji FROM anime WHERE id = %s", (anime_id,))
    anime = cursor.fetchone()
    cursor.close()
    return render_template('watchlist_edit.html', entry=entry, user=user, anime=anime, user_id=user_id, anime_id=anime_id)


@app.route('/watchlist/delete/<int:user_id>/<int:anime_id>')
def watchlist_delete(user_id, anime_id):
    try:
        watchlist_entry_gw.delete(user_id, anime_id)
        flash('Watchlist entry deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('watchlist'))


@app.route('/history')
def history_list():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('history_list.html', users=users)


@app.route('/history/<int:user_id>')
def history(user_id):
    entries = watchlist_history_gw.select_by_user_id(user_id)
    return render_template('history.html', entries=entries, user_id=user_id)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer_anime():
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        from_user_id = int(request.form['from_user_id'])
        to_user_id = int(request.form['to_user_id'])
        anime_id = int(request.form['anime_id'])
        
        try:
            conn.autocommit = False
            
            cursor.execute("""
                SELECT state, rating, progress FROM watchlist_entries 
                WHERE user_id = %s AND anime_id = %s
            """, (from_user_id, anime_id))
            entry = cursor.fetchone()
            
            if not entry:
                conn.rollback()
                flash('Source user does not have this anime in watchlist', 'error')
                return redirect(url_for('transfer_anime'))
            
            cursor.execute("""
                SELECT 1 FROM watchlist_entries 
                WHERE user_id = %s AND anime_id = %s
            """, (to_user_id, anime_id))
            if cursor.fetchone():
                conn.rollback()
                flash('Target user already has this anime in watchlist', 'error')
                return redirect(url_for('transfer_anime'))
            
            cursor.execute("""
                DELETE FROM watchlist_entries 
                WHERE user_id = %s AND anime_id = %s
            """, (from_user_id, anime_id))
            
            cursor.execute("""
                INSERT INTO watchlist_entries (user_id, anime_id, state, rating, progress)
                VALUES (%s, %s, %s, %s, %s)
            """, (to_user_id, anime_id, entry[0], entry[1], entry[2]))
            
            conn.commit()
            flash(f'Anime successfully transferred from user {from_user_id} to user {to_user_id}', 'success')
            return redirect(url_for('watchlist'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Transaction failed: {e}', 'error')
    
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title_romaji FROM anime")
    anime = cursor.fetchall()
    cursor.close()
    
    return render_template('transfer.html', users=users, anime=anime)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
