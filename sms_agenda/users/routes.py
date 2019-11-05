import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sms_agenda import db, bcrypt, mail
from sms_agenda.models import User, Post
from sms_agenda.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, SMSForm)
from sms_agenda.users.utils import send_reset_email
from flask_mail import Message
import sqlite3
from sqlite3 import Error

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, phone='+1', timezone='UTC', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/sms", methods=['GET', 'POST'])
@login_required
def sms():
    form = SMSForm()
    id = current_user.id
    phone = form.phone.data
    timezone = form.timezone.data
    if form.validate_on_submit():
        conn = sqlite3.connect('sms_agenda/users.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE user SET phone = ? WHERE id = ? ''', (phone, id))
        cursor.execute('''UPDATE user SET timezone = ? WHERE id = ? ''', (timezone, id))
        conn.commit()
        cursor.close()
        flash(f'The SMS notifications are now set up', 'success')
    return render_template('sms.html', title='SMS', form=form)


# @users.route("/send_all", methods=['GET', 'POST'])
# @login_required
# def send():
#     connection = sqlite3.connect("sms_agenda/users.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT phone, timezone FROM user;")
#     result = cursor.fetchall()
#     now = datetime.datetime.utcnow()
#     for phone, timezone in result:
#         if now + int(timezone) = 10:
#             send_sms(phone, get_agenda(int(timezone)))
#     cursor.close()
#     connection.close()


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with password instructions has been sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your has been updated, you can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
