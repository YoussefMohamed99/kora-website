from datetime import date, datetime, timedelta
import os

from flask import Flask, jsonify, render_template, url_for, redirect, flash
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
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(50))


class Comment(db.Model):
    __table_name__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False, nullable=False)

@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():

    # db.session.add(Comment(text='bla bla blo'))
    # db.session.commit()

    form = forms.NewComment()
    in7days = date.today() - timedelta(days=7)
    in1month = date.today() - timedelta(days=30)
    in1year = date.today() - timedelta(days=365)
    database_today = Comment.query.filter(Comment.date >= date.today()).all()
    database_last_week = Comment.query.filter(Comment.date < date.today(), Comment.date >= in7days).all()
    database_last_month = Comment.query.filter(Comment.date < in7days, Comment.date >= in1month).all()
    database_last_year = Comment.query.filter(Comment.date < in1month, Comment.date >= in1year).all()
    database_past = Comment.query.filter(Comment.date < in1year).all()
    context = {
        'form':form,
        'database_today':database_today,
        'database_last_week':database_last_week,
        'database_last_month':database_last_month,
        'database_last_year':database_last_year,
        'database_past':database_past
    }
    if form.validate_on_submit():
        comment = Comment(text=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index', **context))
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    context = {'form':form}
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if not user:
            flash('Wrong username or password')
            return render_template('login.html', **context)
        else:
            return redirect(url_for('admin_page'))
    return render_template('login.html', **context)


# @app.route('/admin/<name>', methods=['GET', 'POST'])
# def admin_page(name):
#     removeform = forms.AdminRemoveForm()
