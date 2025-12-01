import os

class config:

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hello"

    #MYSQL_USER = "root"
    #MYSQL_PASSWORD = ""
    #MYSQL_HOST = "127.0.0.1"
    #MYSQL_DB = "realstate"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "DB#cbAIrr!5PW"
    MYSQL_HOST = "165.227.220.96"
    MYSQL_DB = "realstate"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'mysql + pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

        
    LOGIN_DISABLED = False

    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # Gets the API Key from .env
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # Gets the Secret Key from .env
    
    # This is the "From" address and name that will appear in the recipient's inbox
    MAIL_DEFAULT_SENDER = ('RealState Platform', 'basheer@etdv.org')