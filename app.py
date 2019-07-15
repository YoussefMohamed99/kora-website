from datetime import datetime

from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import forms
import models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'never been easier'
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.NewUserForm()
    if form.validate_on_submit():
        user = models.User.create(username=form.username.data)
        flash(f'{user.username.capitalize()} your data has been saved in my database!')
        return redirect(url_for('hello', name=user.username))
    context= {
        'form': form,
        'current_time': datetime.utcnow()
    }
    return render_template('signup.html', **context)
