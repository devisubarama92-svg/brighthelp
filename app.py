from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------------------------------
# DATABASE INIT
# -------------------------------
def init_db():
    conn = sqlite3.connect('brighthelp.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            help_type TEXT,
            description TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------------
# LOGIN PAGE
# -------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

# -------------------------------
# REGISTER PAGE
# -------------------------------
@app.route('/register')
def register():
    return render_template('register.html')

# -------------------------------
# REQUEST HELP
# -------------------------------
@app.route('/request-help', methods=['GET', 'POST'])
def request_help():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        help_type = request.form.get('help_type')
        description = request.form.get('description')

        # ALWAYS SET DEFAULT STATUS
        status = 'Pending'

        conn = sqlite3.connect('brighthelp.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO requests (name, location, help_type, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, location, help_type, description, status))

        conn.commit()
        conn.close()

        return redirect('/view-requests')

    return render_template('request_help.html')

# -------------------------------
# VIEW REQUESTS
# -------------------------------
@app.route('/view-requests')
def view_requests():
    conn = sqlite3.connect('brighthelp.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM requests')
    requests_data = cursor.fetchall()

    conn.close()

    return render_template('view_requests.html', requests=requests_data)

# -------------------------------
# ACCEPT REQUEST
# -------------------------------
@app.route('/accept/<int:id>')
def accept_request(id):
    conn = sqlite3.connect('brighthelp.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE requests SET status='Accepted' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view-requests')

# -------------------------------
# COMPLETE REQUEST
# -------------------------------
@app.route('/complete/<int:id>')
def complete_request(id):
    conn = sqlite3.connect('brighthelp.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE requests SET status='Done' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view-requests')

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)