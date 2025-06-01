from flask import Blueprint,redirect,render_template,request,session,url_for,flash
from werkzeug.security import check_password_hash
import sqlite3

login_bp = Blueprint("login_bp", __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        with sqlite3.connect("predictions.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name,role, password FROM users WHERE name = ?", (name,))
            user = cursor.fetchone()
        if user:
            user_id, name,role, hashed_password = user
            if check_password_hash(hashed_password, password):
                session["id"] = user_id
                session["name"] = name
                session["role"] = role
                flash(f"Welcome, {name}!", "success")
                return redirect(url_for("main_app.index"))
            else:
                flash("Incorrect password!", "danger")
        else:
            flash("No account found with this email!", "danger")

    return render_template("login.html")