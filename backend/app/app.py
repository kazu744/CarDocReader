from flask import Flask, render_template
from flask_login import LoginManager
from app.form import SignupForm
from app.models.User import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

def hello():
    return "Hello, World!"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm
    return render_template('signup.html', form=form)
