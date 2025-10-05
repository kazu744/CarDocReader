from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

class SignupForm(FlaskForm):
    email = EmailField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("パスワード再入力", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('登録')

class LoginForm(FlaskForm):
    email = EmailField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField('ログイン')

class ProfileEditForm(FlaskForm):
    email = EmailField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード")
    confirm_password = PasswordField("パスワード再入力", validators=[EqualTo("password")])
    vision_api = TextAreaField("Vision API")
    openai_api = TextAreaField("OpenAI API")
    submit = SubmitField('更新')

    def validate_password(self, password):
        if password.data and len(password.data) < 8:
            raise ValidationError("8文字以上で入力してください")