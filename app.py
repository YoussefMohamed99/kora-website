from datetime import datetime
import os

from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

import forms

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(50))


class Comment(db.Model):
    __table__name = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    text = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean(), default=False, nullable=False)

@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.NewComment()
    context = {
        'form':form
    }
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index', **context))
    return render_template('index.html', **context)
