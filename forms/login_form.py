from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired()])
    surname = StringField('Введите фамилию', validators=[DataRequired()])
    email = EmailField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторить пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться', validators=[DataRequired()])