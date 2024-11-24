from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    con= sqlite3.connect("newusers.db")
    return con

def create_table():
    con= create_connection()
    cur= con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS newuser(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, username TEXT, password TEXT, number TEXT, email TEXT)''')
    con.commit()
    con.close()
    return redirect("/admin")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(username, password) VALUES(?, ?)''', (username, password))
        con.commit()
        cur.close()
        print(f"Received: Username={username}, Password={password}")
        return redirect('/about')
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])

def register():
    if request.method == "POST":
        email = request.form.get("email")
        DOB = request.form.get("DOB")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(email, DOB) VALUES(?, ?)''', (email, DOB))
        user = cur.fetchone()
        con.commit()
        cur.close()
        print(f"Received: Email={email}, DOB={DOB}")
        return redirect('/login')
    return render_template("registration.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

if __name__ == "__main__":
    create_connection()
    create_table()
    app.run(debug=True)