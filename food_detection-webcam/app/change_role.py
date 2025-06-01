from flask import Blueprint, url_for, redirect, request, render_template, flash, session
import sqlite3

change_roles = Blueprint("change_roles", __name__)

@change_roles.route("/change_role/<int:user_id>", methods=["POST", "GET"])
def change_role(user_id):
    if request.method == "POST":
        role = request.form.get("update_role")
        
        # Debugging session role
        print(f"Session role: {session.get('role')}")  # Check what's stored in the session

        if session.get("role") and session.get("role").lower() == "admin":
            try:
                conn = sqlite3.connect("predictions.db")
                cur = conn.cursor()
                cur.execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
                conn.commit()
                flash(f"User role updated to {role} successfully!", "success")
            except sqlite3.Error as e:
                flash(f"Database error: {e}", "danger")
            finally:
                conn.close()
            
            return redirect(url_for("all_user.all_users"))
        else:
            flash("You are not authorized to change roles.", "danger")
    
    return render_template("users.html")
