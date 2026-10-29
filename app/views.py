import logging
import os
from flask import render_template, request, redirect, url_for, flash
from . import app
from .forms import ContactForm

contact_logger = logging.getLogger('contact_logger')
contact_logger.setLevel(logging.INFO)

if not contact_logger.handlers:
    log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(log_dir, 'contact.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    contact_logger.addHandler(file_handler)


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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_logger.info(
            f"Успішна відправка форми: Name='{form.name.data}', Email='{form.email.data}', "
            f"Phone='{form.phone.data}', Subject='{form.subject.data}', Message='{form.message.data}'"
        )
        flash("Ваше повідомлення успішно надіслано та збережено!", "success")
        return redirect(url_for('contact'))

    if request.method == 'POST':
        contact_logger.warning(
            f"Неуспішна спроба відправки форми: помилки={form.errors}"
        )
        flash("Помилка відправлення форми. Будь ласка, перевірте введені дані.", "danger")

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
