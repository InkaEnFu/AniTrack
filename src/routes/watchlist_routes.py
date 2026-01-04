from flask import Blueprint, render_template, request, redirect, url_for, flash
from connection import DatabaseConnection
from tables.watchlist_entry_gateway import WatchlistEntryGateway
from tables.watchlist_history_gateway import WatchlistHistoryGateway

watchlist_bp = Blueprint('watchlist', __name__)

db = DatabaseConnection()
watchlist_entry_gw = WatchlistEntryGateway()
watchlist_history_gw = WatchlistHistoryGateway()


@watchlist_bp.route('/watchlist')
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


@watchlist_bp.route('/watchlist/add', methods=['GET', 'POST'])
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
            return redirect(url_for('watchlist.watchlist'))
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


@watchlist_bp.route('/watchlist/edit/<int:user_id>/<int:anime_id>', methods=['GET', 'POST'])
def watchlist_edit(user_id, anime_id):
    if request.method == 'POST':
        status = request.form['status']
        score = int(request.form['score']) if request.form.get('score') else None
        progress = int(request.form.get('progress') or 0)
        
        try:
            watchlist_entry_gw.update(user_id, anime_id, status, score, progress)
            flash('Watchlist entry updated successfully', 'success')
            return redirect(url_for('watchlist.watchlist'))
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


@watchlist_bp.route('/watchlist/delete/<int:user_id>/<int:anime_id>')
def watchlist_delete(user_id, anime_id):
    try:
        watchlist_entry_gw.delete(user_id, anime_id)
        flash('Watchlist entry deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('watchlist.watchlist'))


@watchlist_bp.route('/history')
def history_list():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('history_list.html', users=users)


@watchlist_bp.route('/history/<int:user_id>')
def history(user_id):
    entries = watchlist_history_gw.select_by_user_id(user_id)
    return render_template('history.html', entries=entries, user_id=user_id)


@watchlist_bp.route('/transfer', methods=['GET', 'POST'])
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
                return redirect(url_for('watchlist.transfer_anime'))
            
            cursor.execute("""
                SELECT 1 FROM watchlist_entries 
                WHERE user_id = %s AND anime_id = %s
            """, (to_user_id, anime_id))
            if cursor.fetchone():
                conn.rollback()
                flash('Target user already has this anime in watchlist', 'error')
                return redirect(url_for('watchlist.transfer_anime'))
            
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
            return redirect(url_for('watchlist.watchlist'))
            
        except Exception as e:
            conn.rollback()
            flash(f'Transaction failed: {e}', 'error')
    
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title_romaji FROM anime")
    anime = cursor.fetchall()
    cursor.close()
    
    return render_template('transfer.html', users=users, anime=anime)
