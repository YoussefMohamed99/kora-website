from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, SelectField


class NewComment(FlaskForm):
    comment = StringField(
        'comment', [
        validators.Length(max=500),
        validators.InputRequired()
        ])
    post = SubmitField('Post')


class Subscribe(FlaskForm):
    gmail = SubmitField('Subscribe on Gmail')
    #messenger = SubmitField('Subscribe on Messenger')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=20, min=3), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')


class AdminRemoveForm(FlaskForm):
    comment = SelectField(f'comment: ')
    submit = SubmitField('Remove')
