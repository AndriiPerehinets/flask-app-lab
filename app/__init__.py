from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pymongo import MongoClient
from .config import config

db = SQLAlchemy()
migrate = Migrate()

client = MongoClient('mongodb://LoterVise:goodpassword@localhost:27017/?authSource=admin')
mongo_db = client['lab5_db']
products_collection = mongo_db['products']


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    from .views import init_views
    init_views(app)

    from .users.views import users_bp
    from .products.views import products_bp
    from .posts import post_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp)

    return app

