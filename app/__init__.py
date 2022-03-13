import os
from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "app.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_NAME
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .main import main
    from .auth import auth
    from .user import user

    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(user, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.before_request
    def before_request():
        g.user = current_user
        g.authenticated = current_user.is_authenticated

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template("404.html"), 404

    return app


def create_database(app):
    if not os.path.exists("app/" + DB_NAME):
        db.create_all(app=app)
