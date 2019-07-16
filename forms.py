from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, validators


class NewComment(FlaskForm):
    comment = StringField(
        'comment', [
        validators.Length(max=500),
        validators.InputRequired()
        ])
    submit = SubmitField('Submit')
