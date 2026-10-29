import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lab5_secret_key_flashing_and_sessions')
app.secret_key = app.config['SECRET_KEY']

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://LoterVise:goodpassword@localhost:27017/?authSource=admin')
app.config['MONGO_URI'] = MONGO_URI

client = MongoClient(MONGO_URI)
db = client['lab5_db']
products_collection = db['products']

from . import views

from .users.views import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from .products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')
