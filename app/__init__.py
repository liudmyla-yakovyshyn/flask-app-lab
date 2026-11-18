import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .config import config_map

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "dev")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .users import users_bp
        app.register_blueprint(users_bp)

        from .products import products_bp
        app.register_blueprint(products_bp)

        from .posts import post_bp
        from .posts import models
        app.register_blueprint(post_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()
