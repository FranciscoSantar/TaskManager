from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.path.join(os.getcwd(), 'data', 'database.db')

db = SQLAlchemy()

def create_app(testing=False) -> Flask:
    app = Flask(__name__)
    #app config
    app.config['TESTING'] = testing
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    #import routers
    from app.routes.task import task_router
    from app.routes.users import user_router
    #Config documentation
    SWAGGER_URL = '/docs'
    API_URL = '/static/docs.yml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Task Manager application"
        }
    )
    #Authentication setup
    JWTManager(app)
    #Database Setup
    db.init_app(app)

    app.register_blueprint(blueprint=task_router)
    app.register_blueprint(blueprint=user_router)
    app.register_blueprint(swaggerui_blueprint)
    return app