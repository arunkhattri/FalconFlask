from flask import render_template
from app import app


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
