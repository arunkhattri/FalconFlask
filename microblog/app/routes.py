from flask import render_template, flash, redirect, url_for
from flask import request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)


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
        # redirect back from successful login to the page the user wanted
        # to access.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
