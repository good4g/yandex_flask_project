from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class EnterForm(FlaskForm):
    email = EmailField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти', validators=[DataRequired()])