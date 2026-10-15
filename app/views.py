from flask import render_template, request
from . import app

@app.route('/')
def resume():
    return render_template('index.html')

@app.route('/homepage')
def home():
    """View for the Home page of your website."""

    agent = request.user_agent 

    return render_template("index.html", agent=agent)