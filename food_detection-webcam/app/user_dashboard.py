from flask import Blueprint,flash,render_template,redirect,url_for,session
import sqlite3
user_dash = Blueprint("user", __name__)

@user_dash.route("/user_dashboard")
def user_dashboard():
    if "id" not in session:  # Ensure the user is logged in
        flash("You must be logged in to access the dashboard.", "danger")
        return redirect(url_for("login_bp.login"))

    user_id = session.get("id")  # Get the logged-in user's ID


    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

        # Fetch only the predictions for the current user
    cursor.execute("""
            SELECT food_type, country, confidence, description, nutrients, timestamp
            FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))
    predictions = cursor.fetchall()
    conn.close()

    return render_template("user_dashboard.html", predictions=predictions)