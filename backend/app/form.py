from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, PasswordField, SubmitField, StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

class SignupForm(FlaskForm):
    email = EmailField("メールアドレス", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("パスワード再入力", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('登録')

    def validate_password(self, password):
        if password.data and len(password.data) < 8:
            raise ValidationError("8文字以上で入力してください")
        
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
        
class UploadForm(FlaskForm):
    new_owner_inkan = FileField("新所有者印鑑証明", validators=[FileAllowed(['png', 'jpeg', 'jpg', 'pdf'], 'PDF/PNG/JPEGのみアップロード可能です')])
    submit = SubmitField("アップロード")

class OcrEditForm(FlaskForm):
    new_owner_name = StringField("新所有者氏名")
    new_owner_address_main = StringField("新所有者住所")
    new_owner_address_street = StringField("新所有者丁目")
    new_owner_address_number = StringField("新所有者番地")
    submit = SubmitField("更新")

class OcrDeleteForm(FlaskForm):
    pass