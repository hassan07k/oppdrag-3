import sqlite3
import uuid
from flask import Flask, render_template, request, session, g, flash
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

@app.route("/quiz")
def quiz():
    return render_template("quiz.htm")

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
            return render_template("quiz.htm")
        else:
            flash("Invalid credentials!", "error")
            return render_template("logginn.htm")
    
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
            return render_template("logginn.htm")
        except sqlite3.IntegrityError:
            flash("Email already registered!", "error")
            return render_template("registrering.htm")
    
    return render_template("registrering.htm")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
