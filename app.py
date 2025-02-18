from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_path = os.path.join(os.getcwd(), 'data', 'database.db')

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    from routes.task import task_route
    app.register_blueprint(blueprint=task_route)
    return app