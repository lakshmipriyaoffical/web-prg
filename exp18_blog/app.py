import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, abort

app = Flask(__name__)
app.secret_key = "change-this-secret"
DB = "blog.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, author TEXT NOT NULL, content TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.route("/")
def index():
    with get_db() as conn:
        posts = conn.execute("SELECT * FROM posts ORDER BY created DESC, id DESC").fetchall()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def post(id):
    with get_db() as conn:
        p = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    if not p:
        abort(404)
    return render_template("post.html", p=p)

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        f = request.form
        with get_db() as conn:
            conn.execute("INSERT INTO posts(title,author,content) VALUES(?,?,?)",
                         (f["title"], f["author"], f["content"]))
        flash("Post published.")
        return redirect(url_for("index"))
    return render_template("form.html", p=None)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    with get_db() as conn:
        p = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
        if not p:
            abort(404)
        if request.method == "POST":
            f = request.form
            conn.execute("UPDATE posts SET title=?, author=?, content=? WHERE id=?",
                         (f["title"], f["author"], f["content"], id))
            flash("Post updated.")
            return redirect(url_for("post", id=id))
    return render_template("form.html", p=p)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
