from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages, abort, request
from blog import app, mail
from blog.users.forms import RegisterForm, LoginForm, UpdateProfileForm, ResetForm, ResetPasswordForm
from blog.models import User, Post
from blog import db
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from flask_mail import Message
from flask import Blueprint

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, passwordHash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged as {user_to_create.username}', category='success')
        return redirect(url_for('main.home_page'))
    if form.errors != {}:  # if there ara not errors from the validations
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='danger')
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():

        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user(attempted_user)

            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@users.route('/logout')
def logout_page():
    logout_user()
    flash("You have been log out!", category='info')
    return redirect(url_for('main.home_page'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    posts = current_user.posts

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' + current_user.image_file)

    return render_template('profile.html', title='Account', image_file=image_file, form=form, posts=posts)


@app.route("/user/<string:username>")
@login_required
def username_page(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@techblog.com', recipients=[user])
    msg.body = '''If y

    '''


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = ResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is invalid or expired link', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    return render_template('reset_token.html', title='Reset Password', form=form)
