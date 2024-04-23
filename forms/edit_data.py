from wtforms import TextAreaField, StringField, validators, SubmitField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class EditData(FlaskForm):
    rename = StringField(validators=[DataRequired()])
    re_surname = StringField(validators=[DataRequired()])
    update = SubmitField()