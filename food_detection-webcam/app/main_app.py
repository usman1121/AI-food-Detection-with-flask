
from flask import Blueprint, flash, render_template, url_for, redirect, session

main_app = Blueprint("main_app",__name__)

@main_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_bp.login'))

@main_app.route('/')
def index():
    name = session.get("name")
    if not session.get("id"):
        return redirect(url_for("login_bp.login"))
    flash(f"Welcome, {name}!", "success")
    return render_template('index.html')

@main_app.route("/capture")
def capture():
    return render_template('capture.html')

@main_app.route("/about")
def about():
    return render_template("about.html")





