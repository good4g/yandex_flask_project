from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class CommentForm(FlaskForm):
    comment = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()