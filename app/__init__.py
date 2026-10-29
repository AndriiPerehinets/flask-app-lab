from flask import Flask

app = Flask(__name__)
app.secret_key = 'lab4_secret_key_flashing_and_sessions'

from . import views

from .users.views import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from .products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')
