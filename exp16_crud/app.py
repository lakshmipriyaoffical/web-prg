import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret"
DB = "students.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL, course TEXT NOT NULL)""")

@app.route("/")                       # READ (all)
def index():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM students").fetchall()
    return render_template("index.html", rows=rows)

@app.route("/add", methods=["GET", "POST"])   # CREATE
def add():
    if request.method == "POST":
        with get_db() as conn:
            conn.execute("INSERT INTO students(name,email,course) VALUES(?,?,?)",
                         (request.form["name"], request.form["email"], request.form["course"]))
        flash("Record added.")
        return redirect(url_for("index"))
    return render_template("form.html", rec=None)

@app.route("/edit/<int:id>", methods=["GET", "POST"])   # UPDATE
def edit(id):
    with get_db() as conn:
        rec = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
        if not rec:
            flash("Record not found.", "error")
            return redirect(url_for("index"))
        if request.method == "POST":
            conn.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                         (request.form["name"], request.form["email"], request.form["course"], id))
            flash("Record updated.")
            return redirect(url_for("index"))
    return render_template("form.html", rec=rec)

@app.route("/delete/<int:id>", methods=["POST"])        # DELETE
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE id=?", (id,))
    flash("Record deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
