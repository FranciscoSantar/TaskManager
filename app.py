from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_path = os.path.join(os.getcwd(), 'data', 'database.db')

db = SQLAlchemy()

def create_app(testing=False) -> Flask:
    app = Flask(__name__)
    app.config['TESTING'] = testing
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    db.init_app(app)
    from routes.task import task_router
    from routes.users import user_router
    app.register_blueprint(blueprint=task_router)
    app.register_blueprint(blueprint=user_router)
    return app