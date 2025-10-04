from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from . import settings
from app.form import SignupForm, LoginForm
from app.models.User import User

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

def hello():
    return "Hello, World!"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User.signup(
            email = form.email.data,
            password = form.password.data,
            )
        if new_user:
            flash("登録完了しました")
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(email=form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('ログインに成功しました。')
            return redirect(url_for('home'))
        else:
            flash('ユーザー名またはパスワードが無効です。')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))