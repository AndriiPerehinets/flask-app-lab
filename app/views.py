import logging
from flask import render_template, request, redirect, url_for, flash
from . import app
from .forms import ContactForm

contact_logger = logging.getLogger('contact')
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    handler = logging.FileHandler('feedback.log', encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    contact_logger.addHandler(handler)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_logger.info(f"Контактна форма: {form.name.data}, {form.email.data}, {form.phone.data}, {form.subject.data}, {form.message.data}")
        flash("Ваше повідомлення успішно надіслано!", "success")
        return redirect(url_for('contact'))
    elif request.method == 'POST':
        flash("Помилка відправки форми. Перевірте введені дані.", "danger")
    return render_template("contact.html", form=form)

@app.route('/login')
def login_redirect():
    return redirect(url_for('users.login'))

@app.route('/profile')
def profile_redirect():
    return redirect(url_for('users.profile'))

@app.route('/logout')
def logout_redirect():
    return redirect(url_for('users.logout'))
