from flask import Flask

app = Flask(__name__)

from . import views

# Імпортуємо та реєструємо блюпринт users
from .users.views import users_bp
app.register_blueprint(users_bp, url_prefix='/users')