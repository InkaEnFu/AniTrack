from flask import Blueprint, render_template, request, redirect, url_for, flash
from connection import DatabaseConnection
from tables.anime_gateway import AnimeGateway
from tables.anime_genre_gateway import AnimeGenreGateway
from tables.genre_gateway import GenreGateway

anime_bp = Blueprint('anime', __name__)

db = DatabaseConnection()
anime_gw = AnimeGateway()
anime_genre_gw = AnimeGenreGateway()
genre_gw = GenreGateway()


def validate_required(form, fields):
    for field in fields:
        if field not in form or not form[field].strip():
            return False, f"Field '{field}' is required"
    return True, None


@anime_bp.route('/anime')
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


@anime_bp.route('/anime/add', methods=['GET', 'POST'])
def anime_add():
    if request.method == 'POST':
        valid, error = validate_required(request.form, ['title_romaji', 'status'])
        if not valid:
            flash(error, 'error')
            return render_template('anime_add.html', genres=genre_gw.select_all())
        
        title_romaji = request.form['title_romaji'].strip()
        title_english = request.form.get('title_english', '').strip() or None
        status = request.form['status']
        start_date = request.form.get('start_date') or None
        genre_ids = request.form.getlist('genres')
        
        try:
            episodes = int(request.form.get('episodes') or 0)
            if episodes < 0:
                raise ValueError("Episodes cannot be negative")
        except ValueError as e:
            flash(f'Invalid episodes value: {e}', 'error')
            return render_template('anime_add.html', genres=genre_gw.select_all())
        
        try:
            external_score = float(request.form['external_score']) if request.form.get('external_score') else None
            if external_score is not None and (external_score < 0 or external_score > 10):
                raise ValueError("Score must be between 0 and 10")
        except ValueError as e:
            flash(f'Invalid score value: {e}', 'error')
            return render_template('anime_add.html', genres=genre_gw.select_all())
        
        try:
            new_id = anime_gw.insert(title_romaji, status, title_english, episodes, start_date, external_score)
            for genre_id in genre_ids:
                anime_genre_gw.insert(new_id, int(genre_id))
            flash(f'Anime added successfully with ID: {new_id}', 'success')
            return redirect(url_for('anime.anime_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    genres = genre_gw.select_all()
    return render_template('anime_add.html', genres=genres)


@anime_bp.route('/anime/edit/<int:id>', methods=['GET', 'POST'])
def anime_edit(id):
    if request.method == 'POST':
        title_romaji = request.form['title_romaji']
        title_english = request.form.get('title_english') or None
        episodes = int(request.form.get('episodes') or 0)
        status = request.form['status']
        start_date = request.form.get('start_date') or None
        external_score = float(request.form['external_score']) if request.form.get('external_score') else None
        genre_ids = request.form.getlist('genres')
        
        try:
            anime_gw.update(id, title_romaji, status, title_english, episodes, start_date, external_score)
            anime_genre_gw.delete_by_anime_id(id)
            for genre_id in genre_ids:
                anime_genre_gw.insert(id, int(genre_id))
            flash('Anime updated successfully', 'success')
            return redirect(url_for('anime.anime_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    anime = anime_gw.select_by_id(id)
    genres = genre_gw.select_all()
    current_genres = anime_genre_gw.select_by_anime_id(id)
    return render_template('anime_edit.html', anime=anime, genres=genres, current_genres=current_genres)


@anime_bp.route('/anime/delete/<int:id>')
def anime_delete(id):
    try:
        anime_gw.delete(id)
        flash('Anime deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('anime.anime_list'))
