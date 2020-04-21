from MyApp.config import Config
from flask import Flask
import pyrebase

firebase = pyrebase.initialize_app(Config.firebase_config)
db = firebase.database()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    

    from MyApp.admin.routes import admin
    from MyApp.main.routes import main

    app.register_blueprint(admin)
    app.register_blueprint(main)

    return app