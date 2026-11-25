from flask import Blueprint, render_template, request, url_for, redirect, flash, session, make_response
from flask_login import login_user, login_required, current_user, logout_user
from app import db, bcrypt
from .models import User
from .forms import RegistrationForm, LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates')

# Заглушки для автентифікації користувачів (без бази даних)
USERS_DATA = {
    "admin": "admin123",
    "student": "pass123",
    "user": "password"
}

@users_bp.route("/hi/<string:name>") 
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalars(db.select(User).where(User.email == form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You logged in successfully!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Невірний email або пароль. Спробуйте ще раз.', 'danger')

    return render_template('users/login.html', form=form, title='Login')


@users_bp.route('/account')
@login_required
def account():
    return render_template('users/account.html', user=current_user)


@users_bp.route('/list')
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template('users/users_list.html', users=users)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form, title='Register')

@users_bp.route('/profile')
def profile():
    """Сторінка профілю користувача (Вимоги 3, 6, 7)."""
    if 'username' not in session:
        flash('Помилка доступу: сесія недоступна. Будь ласка, спочатку увійдіть у систему!', 'danger')
        return redirect(url_for('users.login'))

    username = session['username']
    cookies = request.cookies
    theme = request.cookies.get('profile_theme') or session.get('profile_theme', 'light')
    return render_template('users/profile.html', username=username, cookies=cookies, theme=theme)

@users_bp.route('/set-theme/<string:theme_name>', methods=['GET', 'POST'])
def set_theme(theme_name):
    """Маршрут вибору та збереження кольорової схеми (Вимога 7)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для зміни теми!', 'danger')
        return redirect(url_for('users.login'))

    valid_themes = ['light', 'dark', 'blue']
    if theme_name not in valid_themes:
        theme_name = 'light'

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('profile_theme', theme_name, max_age=30 * 24 * 60 * 60)
    session['profile_theme'] = theme_name
    flash(f'Колірну схему успішно змінено на: "{theme_name}"!', 'success')
    return response

@users_bp.route('/cookie/add', methods=['POST'])
def add_cookie():
    """Додавання кукі за ключем, значенням та терміном дії (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()
    value = request.form.get('value', '').strip()
    expires_str = request.form.get('expires', '').strip()

    if not key:
        flash('Помилка: назва (ключ) cookie не може бути порожньою!', 'danger')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))

    max_age = None
    if expires_str:
        try:
            max_age = int(expires_str)
            if max_age <= 0:
                flash('Помилка: термін дії повинен бути додатним числом!', 'danger')
                return redirect(url_for('users.profile'))
        except ValueError:
            flash('Помилка: термін дії має бути цілим числом секунд!', 'danger')
            return redirect(url_for('users.profile'))

    if max_age is not None:
        response.set_cookie(key, value, max_age=max_age)
        flash(f'Cookie "{key}" успішно додано з терміном дії {max_age} сек.!', 'success')
    else:
        response.set_cookie(key, value)
        flash(f'Cookie "{key}" успішно додано на час поточної сесії!', 'success')

    return response

@users_bp.route('/cookie/delete', methods=['POST'])
def delete_cookie():
    """Видалення окремого кукі за вказаним ключем (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('users.login'))

    key = request.form.get('key', '').strip()
    if not key:
        flash('Помилка: вкажіть ключ cookie для видалення!', 'danger')
        return redirect(url_for('users.profile'))

    if key not in request.cookies:
        flash(f'Cookie з ключем "{key}" не знайдено серед поточних cookies.', 'warning')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)
    flash(f'Cookie "{key}" успішно видалено!', 'success')
    return response

@users_bp.route('/cookie/delete-all', methods=['POST'])
def delete_all_cookies():
    """Видалення всіх збережених користувацьких кукі (Вимога 6)."""
    if 'username' not in session:
        flash('Помилка доступу: необхідно увійти у систему для керування cookies!', 'danger')
        return redirect(url_for('users.login'))

    user_keys = [k for k in request.cookies if k != 'session']

    if not user_keys:
        flash('Немає збережених користувацьких cookies для видалення.', 'info')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    for k in user_keys:
        response.delete_cookie(k)

    flash(f'Всі користувацькі cookies ({len(user_keys)}) успішно видалено!', 'success')
    return response

@users_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have successfully logged out.', 'info')
    return redirect(url_for('users.login'))
