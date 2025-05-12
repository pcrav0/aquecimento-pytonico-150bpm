from flask import Flask, render_template, request, g, redirect, url_for
from markupsafe import escape

import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    print('index db = ', db())
    cur = db().cursor()
    posts = list(cur.execute('SELECT * FROM posts'))
    return render_template('index.html', posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.post('/post')
def post():
    name = escape(request.form['name'])
    text = escape(request.form['text'])
    print('post db = ', db())
    cur = db().cursor()
    p = cur.execute('INSERT INTO posts VALUES(?, ?)', (name, text))
    print('insert', p.fetchall())
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# database

DATABASE = 'db/database'

def db():
    result = getattr(g, '_database', None)
    if result is None:
        result = g._database = sqlite3.connect(DATABASE)
    return result

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
