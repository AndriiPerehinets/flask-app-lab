from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from pymongo import MongoClient
from .config import config


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

client = MongoClient('mongodb://LoterVise:goodpassword@localhost:27017/?authSource=admin')
mongo_db = client['lab5_db']
products_collection = mongo_db['products']


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    from .views import init_views
    init_views(app)

    from .users.views import users_bp
    from .users import models as user_models
    from .products.views import products_bp
    from .posts import post_bp
    from .products import models

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp)

    return app


# Екземпляр за замовчуванням для тестів з  минулих лаб
app = create_app()

