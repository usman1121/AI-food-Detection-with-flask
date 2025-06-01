from flask import Blueprint,render_template,redirect,session,url_for
import sqlite3
all_user = Blueprint("all_user", __name__)


@all_user.route("/all_users",methods=["POST","GET"])
def all_users():
    if session.get("role") != "Admin":
        return redirect(url_for("login_bp.login"))
    conn = sqlite3.connect("predictions.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name ,email,role FROM users ")
    users = cur.fetchall()

    return render_template("users.html", users=users)

