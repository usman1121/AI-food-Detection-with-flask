from flask import Blueprint,session,redirect,url_for
import sqlite3

delete_u = Blueprint("delete_u", __name__)
@delete_u.route("/delete_user/<int:user_id>",methods=["POST"])
def delete_user(user_id):
    if session.get("role") != "Admin":
        return redirect(url_for("login_bp.login"))
    conn = sqlite3.connect("predictions.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?",(user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('all_user.all_users'))