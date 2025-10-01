from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class SignupForm(FlaskForm):
    email = EmailField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    confirm_password =PasswordField("パスワード再入力", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('登録')