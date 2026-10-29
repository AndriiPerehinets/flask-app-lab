from flask import render_template, request, redirect, url_for
from . import app

@app.route('/')
@app.route('/home')
@app.route('/homepage')
def home():
    """Головна сторінка веб-сайту."""
    agent = request.user_agent 
    return render_template("index.html", agent=agent)

@app.route('/resume')
def resume():
    """Сторінка резюме."""
    return render_template("resume.html")

# Зручні редіректи для кореневих адрес на модуль users (Users Blueprint)
@app.route('/login')
def login_redirect():
    return redirect(url_for('users.login'))

@app.route('/profile')
def profile_redirect():
    return redirect(url_for('users.profile'))

@app.route('/logout')
def logout_redirect():
    return redirect(url_for('users.logout'))
