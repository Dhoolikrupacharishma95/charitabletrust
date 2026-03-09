# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------------
# Database setup
# ----------------------
def init_db():
    conn = sqlite3.connect("trust.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        reason TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------
# Home page (interface)
# ----------------------
@app.route("/")
def home():
    return render_template("index.html")  # your existing interface HTML

# ----------------------
# Website volunteer submission
# ----------------------
@app.route("/submit_volunteer", methods=["POST"])
def submit_volunteer():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    city = request.form["city"]
    reason = request.form["reason"]

    conn = sqlite3.connect("trust.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO volunteers (name,email,phone,city,reason) VALUES (?,?,?,?,?)",
        (name,email,phone,city,reason)
    )
    conn.commit()
    conn.close()

    return redirect("/")  # go back to home page after submission

# ----------------------
# Admin login page
# ----------------------
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # simple admin credentials
        if username == "admin" and password == "admin123":
            return redirect("/dashboard")
        else:
            return "Invalid credentials. Please go back and try again."

    return render_template("admin_login.html")

# ----------------------
# Admin dashboard
# ----------------------
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    conn = sqlite3.connect("trust.db")
    cursor = conn.cursor()

    # Admin manually adds a volunteer
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]
        reason = request.form["reason"]

        cursor.execute(
            "INSERT INTO volunteers (name,email,phone,city,reason) VALUES (?,?,?,?,?)",
            (name,email,phone,city,reason)
        )
        conn.commit()

    # Fetch all volunteers (from website + admin)
    cursor.execute("SELECT * FROM volunteers")
    volunteers = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", volunteers=volunteers)

# ----------------------
# Run Flask app
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)