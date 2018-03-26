from flask import render_template
from app import app
from app.forms import LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
