from MyApp.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pyrebase
from datetime import date

firebase = pyrebase.initialize_app(Config.firebase_config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

alchemy = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin.admin_login'
login_manager.login_message_category = 'info'

def time(data_time):
    data_time = data_time/1000.0
    timestamp = date.fromtimestamp(data_time)
    return timestamp.strftime("%a %m %d")
def day(data_time):
    return data_time.weekday()


def create_app(config_class=Config):
    global alchemy

    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        alchemy.init_app(app)
    
    login_manager.init_app(app)
    

    from MyApp.admin.routes import admin
    from MyApp.main.routes import main
    from MyApp.messanger.routes import messanger
    from MyApp.foods.routes import foods

    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(messanger)
    app.register_blueprint(foods)

    app.add_template_filter(time)



    return app