import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the db!
db = SQLAlchemy()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # extensions
    db.init_app(app)

    # blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # cli context
    @app.shell_context_processor
    def ctx():
        return { 'app': app, 'db': db }

    return app
