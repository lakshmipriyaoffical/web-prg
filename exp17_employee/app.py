import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret"
DB = "employees.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
            department TEXT NOT NULL, email TEXT NOT NULL, salary REAL NOT NULL)""")

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    with get_db() as conn:
        if q:
            like = f"%{q}%"
            rows = conn.execute("SELECT * FROM employees WHERE name LIKE ? OR emp_id LIKE ?",
                                (like, like)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM employees").fetchall()
    return render_template("index.html", rows=rows, q=q)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        f = request.form
        try:
            with get_db() as conn:
                conn.execute("INSERT INTO employees(emp_id,name,department,email,salary) VALUES(?,?,?,?,?)",
                             (f["emp_id"], f["name"], f["department"], f["email"], float(f["salary"])))
            flash("Employee added.")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Employee ID already exists.", "error")
        except ValueError:
            flash("Salary must be a number.", "error")
    return render_template("form.html", rec=None)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    with get_db() as conn:
        rec = conn.execute("SELECT * FROM employees WHERE id=?", (id,)).fetchone()
        if not rec:
            flash("Employee not found.", "error")
            return redirect(url_for("index"))
        if request.method == "POST":
            f = request.form
            try:
                conn.execute("UPDATE employees SET emp_id=?, name=?, department=?, email=?, salary=? WHERE id=?",
                             (f["emp_id"], f["name"], f["department"], f["email"], float(f["salary"]), id))
                flash("Employee updated.")
                return redirect(url_for("index"))
            except (sqlite3.IntegrityError, ValueError):
                flash("Invalid data or duplicate Employee ID.", "error")
    return render_template("form.html", rec=rec)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with get_db() as conn:
        conn.execute("DELETE FROM employees WHERE id=?", (id,))
    flash("Employee deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
