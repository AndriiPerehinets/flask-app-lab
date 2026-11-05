from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'lab5_secret_key'

client = MongoClient('mongodb://LoterVise:goodpassword@localhost:27017/?authSource=admin')
db = client['lab5_db']
products_collection = db['products']

from . import views
from .users.views import users_bp
from .products.views import products_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
