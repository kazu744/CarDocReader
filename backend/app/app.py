from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from . import settings
from app.form import SignupForm
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
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.signup(form.email.data)
        user.set_password(form.password.data)
        
    return render_template('signup.html', form=form)
