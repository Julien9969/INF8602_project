from flask import Flask, render_template, request, g, redirect, url_for, session
import sqlite3
from functools import wraps

from populate_db import main as populate_db_main

app = Flask(__name__)
DATABASE = 'database.db'
app.config['SECRET_KEY'] = 'secret-key' 

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# --- Index Page ---
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    cursor = conn.cursor()
    search_term = ''
    movies = []

    try:
        if request.method == 'POST':
            search_term = request.form['search']
            # BAD query that is vulnerable to SQL injection
            query = f"SELECT * FROM movies WHERE title LIKE '%{search_term}%'"
            cursor.execute(query)
            movies = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM movies")
            movies = cursor.fetchall()
    except sqlite3.Error as e:
        movies = [{'title': f'Error: {e}', 'rating': ''}]
    finally:
        conn.close()

    return render_template('index.html', movies=movies, search_term=search_term, username=session.get('username'))

# --- User Authentication ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and password == user['password']:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# --- Admin Page ---
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        comment = request.form['comment']
        rating = request.form['rating']
        user = session['username']
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO movies (user, title, comment, rating) VALUES (?, ?, ?, ?)",
                           (user, title, comment, rating))
            db.commit()
            return redirect(url_for('index')) 
        except sqlite3.Error as e:
            error = f"Database error: {e}"
            return render_template('admin.html', error=error)
    return redirect(url_for('admin')) 

if __name__ == '__main__':
    populate_db_main()
    app.run(debug=True)