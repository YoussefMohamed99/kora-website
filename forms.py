from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, validators

class NewUserForm(FlaskForm):
    username = SubmitField('username', [
        validators.InputRequired(),
        validators.Length(max = 30, min = 3)
        ])
    accept_terms = BooleanField(
        'I accept the terms of service', [
            validators.InputRequired()
        ])
    submit = SubmitField('Submit')
