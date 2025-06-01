from flask import Flask
from app.main_app import main_app
from app.admin_dashbaord import admin
from app.all_users import all_user
from app.user_dashboard import user_dash
from app.image_process import procees_image
from app.delete_logs import delete_l
from app.register import register_bp
from app.login import login_bp
from app.delete_users import delete_u
from app.change_role import change_roles


import google.generativeai as genai
def food_detection():
    app = Flask(__name__)
    app.secret_key = 'HSUASA*A&ShhgaA#2@2#$kakjaJjJKKSAHSAHSASNAASASH'
    genai.configure(api_key='#') #replace with your gemini api or google api
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(main_app)
    app.register_blueprint(procees_image)
    app.register_blueprint(admin)
    app.register_blueprint(all_user)
    app.register_blueprint(user_dash)
    app.register_blueprint(delete_l)
    app.register_blueprint(delete_u)
    app.register_blueprint(change_roles)
 

    return app