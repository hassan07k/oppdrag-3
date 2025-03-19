import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
DATABASE = "users.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          full_name TEXT NOT NULL,
                          email TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL)''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/logginn", methods=["GET", "POST"])
def logginn():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for("logginn"))
    
    return render_template("logginn.htm")

@app.route("/registrering", methods=["GET", "POST"])
def registrer():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)", (full_name, email, password))
            db.commit()
            return redirect(url_for("logginn"))
        except sqlite3.IntegrityError:
            flash("Email already registered!", "error")
            return redirect(url_for("registrer"))
    
    return render_template("registrering.htm")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
