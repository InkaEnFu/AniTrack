from flask import Blueprint, render_template, request, redirect, url_for, flash
from mysql.connector import Error as MySQLError
from tables.genre_gateway import GenreGateway

genres_bp = Blueprint('genres', __name__)

genre_gw = GenreGateway()


@genres_bp.route('/genres')
def genre_list():
    genres = genre_gw.select_all()
    return render_template('genres.html', genres=genres)


@genres_bp.route('/genres/add', methods=['GET', 'POST'])
def genre_add():
    if request.method == 'POST':
        name = request.form['name']
        
        try:
            new_id = genre_gw.insert(name)
            flash(f'Genre added successfully with ID: {new_id}', 'success')
            return redirect(url_for('genres.genre_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    return render_template('genre_add.html')


@genres_bp.route('/genres/edit/<int:id>', methods=['GET', 'POST'])
def genre_edit(id):
    if request.method == 'POST':
        name = request.form['name']
        
        try:
            genre_gw.update(id, name)
            flash('Genre updated successfully', 'success')
            return redirect(url_for('genres.genre_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    genre = genre_gw.select_by_id(id)
    return render_template('genre_edit.html', genre=genre)


@genres_bp.route('/genres/delete/<int:id>')
def genre_delete(id):
    try:
        genre_gw.delete(id)
        flash('Genre deleted successfully', 'success')
    except MySQLError as e:
        if e.errno == 1451:
            flash('Cannot delete genre - it is assigned to one or more anime. Remove it from all anime first.', 'error')
        else:
            flash(f'Error: {e}', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('genres.genre_list'))
