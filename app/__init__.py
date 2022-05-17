from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)    
    CORS(app)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app