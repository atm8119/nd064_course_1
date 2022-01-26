import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging, sys

nConnections = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global nConnections 
    nConnections += 1
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define the health-check route of the web application
@app.route('/status')
def healthcheck():
    response = app.response_class(
        response = json.dumps({'result':'OK - healthy'}),
        status = 200,
        mimetype = 'application/json'
    )
    return response

# Define the metrics route of the web application.
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT COUNT(*) FROM posts')
    rowCount = cur.fetchone()[0]
    connection.close()

    response = app.response_class(
        response = json.dumps({'db_connection_count':nConnections,'post_count':rowCount}),
        status = 200,
        mimetype='application/json'
    )
    return response

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('Attempt to access non-existing article. 404 Page returned.')
      return render_template('404.html'), 404
    else:
      app.logger.info('Retrieving article \'' + post[2] + '\'')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us page is being retrieved.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info('Article \'' + title + '\' created and saved.')

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   log_format = '%(levelname)-3s: %(asctime)-3s :: %(message)s'
   date_format='%m/%d/%Y %I:%M:%S %p'
   logging.basicConfig(level=logging.DEBUG)
   
   # Creation of handlers for stdout and stderr output.
   stdout_handler = logging.StreamHandler(sys.stdout)
   stderr_handler = logging.StreamHandler(sys.stderr)
   stdout_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt = date_format))
   stderr_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt = date_format))
   app.logger.addHandler(stdout_handler)
   app.logger.addHandler(stderr_handler)
   app.logger.propagate = False

   app.run(host='0.0.0.0', port='3111')
