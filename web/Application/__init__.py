from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from . import auth
        from . import dashboard

        app.register_blueprint(auth.auth_bp, url_prefix='')
        app.register_blueprint(dashboard.dashboard_bp, url_prefix='')

        return app