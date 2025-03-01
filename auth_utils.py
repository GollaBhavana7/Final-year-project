# auth_utils.py
import sqlite3
from flask import *

DB_PATH = 'signup.db'

# Initialize the database and ensure the table exists
def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                mobile TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        con.commit()

init_db()

def signup():
    username = request.args.get('user', '')
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    number = request.args.get('mobile', '')
    password = request.args.get('password', '')

    # Connect to the database and insert the new user record
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("INSERT INTO info (user, name, email, mobile, password) VALUES (?, ?, ?, ?, ?)",
                (username, name, email, number, password))
    con.commit()
    con.close()

    # Render the signup page with a success message
    return render_template("register.html", message="Registration completed successfully.")


def signin():
    mail1 = request.args.get('user', '')
    password1 = request.args.get('password', '')

    # Static admin credentials check
    if mail1 == 'admin' and password1 == 'admin':
        return redirect(url_for('home'))

    # Database check for other users
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("SELECT `user`, `password` FROM info WHERE `user` = ? AND `password` = ?", (mail1, password1))
    data = cur.fetchone()
    con.close()

    if data:
        # If user is found in the database, redirect to home
        return redirect(url_for('home'))
    else:
        # If credentials are invalid, show an error message
        return render_template("login.html", error="Invalid credentials. Please try again.")

