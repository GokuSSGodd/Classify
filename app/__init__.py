from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'classify.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 1,
        'max_overflow': 0
    }
    db.init_app(app)
    migrate.init_app(app, db)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        db.create_all()
    
    return app
