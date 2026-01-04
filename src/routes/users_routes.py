from flask import Blueprint, render_template, request, redirect, url_for, flash
import re
from connection import DatabaseConnection
from tables.user_gateway import UserGateway

users_bp = Blueprint('users', __name__)

db = DatabaseConnection()
user_gw = UserGateway()


def validate_required(form, fields):
    for field in fields:
        if field not in form or not form[field].strip():
            return False, f"Field '{field}' is required"
    return True, None


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


@users_bp.route('/users')
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


@users_bp.route('/users/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        valid, error = validate_required(request.form, ['username', 'email'])
        if not valid:
            flash(error, 'error')
            return render_template('user_add.html')
        
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        is_admin = 'is_admin' in request.form
        
        if len(username) < 3 or len(username) > 32:
            flash('Username must be between 3 and 32 characters', 'error')
            return render_template('user_add.html')
        
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return render_template('user_add.html')
        
        try:
            new_id = user_gw.insert(username, email, is_admin)
            flash(f'User added successfully with ID: {new_id}', 'success')
            return redirect(url_for('users.user_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    return render_template('user_add.html')


@users_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        is_admin = 'is_admin' in request.form
        
        try:
            user_gw.update(id, username, email, is_admin)
            flash('User updated successfully', 'success')
            return redirect(url_for('users.user_list'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    user = user_gw.select_by_id(id)
    return render_template('user_edit.html', user=user)


@users_bp.route('/users/delete/<int:id>')
def user_delete(id):
    try:
        user_gw.delete(id)
        flash('User deleted successfully', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('users.user_list'))
