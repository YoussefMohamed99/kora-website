from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class NewComment(FlaskForm):
    comment = StringField(
        'comment', [
        validators.Length(max=500),
        validators.InputRequired()
        ])
    post = SubmitField('Post')
