from wtforms import TextAreaField, StringField, validators, SubmitField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class AddPost(FlaskForm):
    title = StringField(validators=[DataRequired(), validators.length(max=70)], default='')
    description = TextAreaField(validators=[DataRequired(), validators.length(max=200)])
    content = TextAreaField(validators=[DataRequired(), validators.length(max=50000000)])
    photo = FileField(name='fieldF')
    submit = SubmitField()
