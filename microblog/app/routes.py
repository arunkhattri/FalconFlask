from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Arun'}
    posts = [
        {
            'author': {'username': "Aarush"},
            'body': 'Beautiful day in Dhanbad'
        },
        {
            'author': {'username': "Aaryaansh"},
            'body': 'Where is my firefox cycle?'
        },
        {
            'author': {'username': "Maira"},
            'body': 'My only concern is Milk'
        }
    ]
    return render_template('index.html', title='Home',
                           user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user logged in, redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # otherwise serve login form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # check if user exist, if yes password matches
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))

        # register the user as logged in.
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
