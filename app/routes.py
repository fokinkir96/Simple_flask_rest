from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from app.forms import LoginForm, UpdateUserForm, UpdatePassword
from flask_login import current_user, login_user,  login_required
from app.models import User
# Register
from app.forms import RegistrationForm
from app import db
# Logout
from flask_login import logout_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Войти'
    if current_user.is_authenticated:
        return redirect(url_for('update_profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('update_profile', username=user.username)

        return redirect(next_page)

    return render_template('login.html', title=title, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Регистрация'
    if current_user.is_authenticated:
        return redirect(url_for('update_profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, вы успешно зарагестрировались на сайте!')
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_required
@app.route('/user/<username>', methods=['GET', 'POST', 'PUT'])
def update_profile(username):
    title = 'Мой профиль'
    form = UpdateUserForm()

    if form.validate_on_submit():
    # if request.method == 'POST':
        db.session.query(User).filter_by(username=current_user.username).update({
            "username": form.username.data,
            "email": form.email.data,
            "phone": form.phone.data,
        })
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Вы успешно изменили свои данные!')
        return redirect(url_for('update_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template('profile.html', title=title, form=form, user=current_user)

@login_required
@app.route('/user/<username>/update_password', methods=['GET', 'POST'])
def update_password(username):
    title = 'Смена пароля'
    user = User.query.filter_by(username=username).first()
    form = UpdatePassword()
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()

        flash('Ваш пароль был успешно изменен!')
        return redirect(url_for('update_password', username=current_user.username))

    return render_template('update.html', title=title, form=form)

@login_required
@app.route('/user/<username>/delete_user', methods=['GET'])
def delete_user(username):
    logout_user()
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))
