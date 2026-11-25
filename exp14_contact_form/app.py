import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret"
DB = "contacts.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL, message TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        message = request.form["message"].strip()
        if not (name and email and message) or "@" not in email:
            flash("Please fill all fields with a valid email.", "error")
            return redirect(url_for("contact"))
        with get_db() as conn:
            conn.execute("INSERT INTO contacts(name,email,message) VALUES(?,?,?)",
                         (name, email, message))
        flash("Thank you! Your message has been submitted.")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/messages")
def messages():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
    return render_template("messages.html", rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
