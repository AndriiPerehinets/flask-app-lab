from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import app

# Заглушки для автентифікації користувачів (без бази даних)
USERS_DATA = {
    "admin": "admin123",
    "student": "pass123",
    "user": "password"
}

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username in USERS_DATA and USERS_DATA[username] == password:
            session['username'] = username
            flash(f'Успішний вхід! Вітаємо, {username}!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Невірний логін або пароль. Спробуйте ще раз.', 'danger')
            return redirect(url_for('login'))

    if 'username' in session:
        return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('Помилка доступу: сесія недоступна. Будь ласка, спочатку увійдіть у систему!', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    cookies = request.cookies
    theme = request.cookies.get('profile_theme') or session.get('profile_theme', 'light')
    return render_template('profile.html', username=username, cookies=cookies, theme=theme)

@app.route('/set-theme/<string:theme_name>', methods=['GET', 'POST'])
def set_theme(theme_name):
    """Окремий маршрут для вибору та збереження кольорової схеми (Вимога 7)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для зміни теми!', 'danger')
        return redirect(url_for('login'))

    valid_themes = ['light', 'dark', 'blue']
    if theme_name not in valid_themes:
        theme_name = 'light'

    response = make_response(redirect(url_for('profile')))

    response.set_cookie('profile_theme', theme_name, max_age=30 * 24 * 60 * 60)
    session['profile_theme'] = theme_name
    flash(f'Колірну схему успішно змінено на: "{theme_name}"!', 'success')
    return response

@app.route('/cookie/add', methods=['POST'])
def add_cookie():
    """Додавання кукі за ключем, значенням та терміном дії (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('login'))

    key = request.form.get('key', '').strip()
    value = request.form.get('value', '').strip()
    expires_str = request.form.get('expires', '').strip()

    if not key:
        flash('Помилка: назва (ключ) cookie не може бути порожньою!', 'danger')
        return redirect(url_for('profile'))

    response = make_response(redirect(url_for('profile')))

    max_age = None
    if expires_str:
        try:
            max_age = int(expires_str)
            if max_age <= 0:
                flash('Помилка: термін дії повинен бути додатним числом!', 'danger')
                return redirect(url_for('profile'))
        except ValueError:
            flash('Помилка: термін дії має бути цілим числом секунд!', 'danger')
            return redirect(url_for('profile'))

    if max_age is not None:
        response.set_cookie(key, value, max_age=max_age)
        flash(f'Cookie "{key}" успішно додано з терміном дії {max_age} сек.!', 'success')
    else:
        response.set_cookie(key, value)
        flash(f'Cookie "{key}" успішно додано на час поточної сесії!', 'success')

    return response

@app.route('/cookie/delete', methods=['POST'])
def delete_cookie():
    """Видалення окремого кукі за вказаним ключем (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('login'))

    key = request.form.get('key', '').strip()
    if not key:
        flash('Помилка: вкажіть ключ cookie для видалення!', 'danger')
        return redirect(url_for('profile'))

    if key not in request.cookies:
        flash(f'Cookie з ключем "{key}" не знайдено серед поточних cookies.', 'warning')
        return redirect(url_for('profile'))

    response = make_response(redirect(url_for('profile')))
    response.delete_cookie(key)
    flash(f'Cookie "{key}" успішно видалено!', 'success')
    return response

@app.route('/cookie/delete-all', methods=['POST'])
def delete_all_cookies():
    """Видалення всіх збережених користувацьких кукі (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('login'))

    user_keys = [k for k in request.cookies if k != 'session']

    if not user_keys:
        flash('Немає збережених користувацьких cookies для видалення.', 'info')
        return redirect(url_for('profile'))

    response = make_response(redirect(url_for('profile')))
    for k in user_keys:
        response.delete_cookie(k)

    flash(f'Всі користувацькі cookies ({len(user_keys)}) успішно видалено!', 'success')
    return response

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = session.pop('username', None)
    if user:
        flash(f'Користувач {user} успішно вийшов із системи.', 'info')
    else:
        flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('login'))
