from flask import Blueprint,request,flash,redirect,url_for,render_template
import sqlite3
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register_bp", __name__)
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        admin_code = request.form["admin_code"]


        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Admin code validation
        ADMIN_SECRET_CODE = "food12345" 

        if role == "Admin" and admin_code != ADMIN_SECRET_CODE:
            flash("Invalid admin code!", "danger")
            return redirect(url_for('register_bp.register'))

        # Insert into database
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO users(name,role,email,password) VALUES(?,?,?,?)",
                               (username,role,email,hashed_password)
        )
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login_bp.login'))

    return render_template('register.html')