from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class SignupForm(FlaskForm):
    email = StringField("メールアドレス")
    password = PasswordField("パスワード")
    repeatpassword =PasswordField("パスワード再入力")
    submit = SubmitField('登録')