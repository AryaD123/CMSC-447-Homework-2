"""
Arya Das
CMSC 447
HW 2
"""

"""from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"
    """
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def database_setup():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (Name TEXT, Id INTEGER PRIMARY KEY, Points INTEGER)''')

    # Using Provided Sample Data in homework instructions
    users = [('Steve Smith', 211, 80),
             ('Jian Wong', 122, 92),
             ('Chris Peterson', 213, 91)
             ('Sai Patel', 524, 94)
             ('Andrew Whitehead', 425, 99)
             ('Lynn Roberts', 626, 90)
             ('Robert Sanders', 287, 75)]

    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO users (Name, Id, Points) VALUES (?, ?, ?)', users)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    user_list = [{'Name': row['Name'], 'Id': row['Id'], 'Points': row['Points']} for row in users]

    conn.close()
    return jsonify(user_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    name = request.form['name']
    id = request.form['id']
    points = request.form['points']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (Name, Id, Points) VALUES (?, ?, ?)', (name, id, points))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_user():
    name = request.args.get('name')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE Name LIKE ?', ('%'+name+'%',)).fetchall()
    conn.close()
    return render_template('search_results.html', users=user)  # You need to create search_results.html

@app.route('/delete', methods=['POST'])
def delete_user():
    id = request.form['id']
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE Id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_user():
    id = request.form['id']
    name = request.form['name']
    points = request.form['points']
    conn = get_db_connection()
    conn.execute('UPDATE users SET Name = ?, Points = ? WHERE Id = ?', (name, points, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)