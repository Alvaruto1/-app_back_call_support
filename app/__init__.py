from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from app.settings import DevelopmentConfig

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    #app.config['CORS_HEADERS'] = 'Content-Type'
    #app.config['SECRET_KEY'] = 'secret-key-goes-here'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    JWTManager(app)
    db.init_app(app)    
    
    
    from app.routes.auth import auth as auth_blueprint
    from app.routes.call_log_routes import call_log as call_log_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(call_log_blueprint)
    


    return app

app= create_app()
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)