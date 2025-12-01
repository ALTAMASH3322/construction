import os

from flask import Flask, jsonify

from flask_cors import CORS
import pymysql
from flask_mail import Mail

from config import config as c

db_config_ = {
    "host": c.MYSQL_HOST,
    "password": c.MYSQL_PASSWORD,
    "user": c.MYSQL_USER,
    "database": c.MYSQL_DB
}




mail = Mail()

def getConnection ():
    return pymysql.connect(
        host= c.MYSQL_HOST,
        user= c.MYSQL_USER,
        database= c.MYSQL_DB,
        password= c.MYSQL_PASSWORD,
        cursorclass= pymysql.cursors.DictCursor
    )

def create_app():
    app = Flask(__name__)
    CORS(app)
    # REPLACE WITH THESE TWO LINES
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
    app.config.from_object('config.config') 

    SALT = "hi-farru-lets-dance-in-a-disco"


    # Initialize mail with the app
    mail.init_app(app)
    from routes.auth import auth_bp
    from routes.agent import agent_bp
    from routes.buyer import buyer_bp
    from routes.chatbot import chat_bp
    from routes.chat import(chat_system)
    from routes.reviews import(review_bp)
    from routes.search import(search_bp)
    from routes.billing import billing_bp  
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(chat_system)
    app.register_blueprint(review_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(admin_bp)

    return app