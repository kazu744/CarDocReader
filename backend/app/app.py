import json
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from . import settings
from app.form import SignupForm, LoginForm, ProfileEditForm, UploadForm, OcrEditForm, OcrDeleteForm
from app.models.User import User
from app.models.Ocr import Ocr
from app.ocr.cloud_vision import detect_text_from_image
from app.openai.openai import extract_structure_data_from_text

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
MAX_FILE_SIZE_MB = 10

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileEditForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        User.profile_edit(
            user_id=current_user.id,
            email=form.email.data,
            password=form.password.data,
            vision_api=form.vision_api.data,
            openai_api=form.openai_api.data,
        )
        return redirect(url_for('profile'))
    else:
        print(f"{form.errors}")
    return render_template('profile_edit.html', user=current_user, form=form)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'GET':
        return render_template('upload.html', form=form)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            if not user.vision_api or not user.openai_api:
                return "エラー: APIキーが設定されていません"
            
        results = []
        ocr_texts = {}

        files = {
            "new_owner_inkan": form.new_owner_inkan.data
        }

        for doc_type, file in files.items():
            if not files or not getattr(file, "filename", None):
                continue

            if not allowed_file(file.filename):
                results.append({"type": doc_type, "status": "error", "message": "拡張子が無効です"})
                continue

            contents = file.read()
            if len(contents) / (1024 * 1024) > MAX_FILE_SIZE_MB:
                results.append({"type": doc_type, "status": "error", "message": "ファイルのサイズが大きすぎます。"})
                continue

            try:
                ocr_result = detect_text_from_image(contents, vision_api=current_user.vision_api)
                ocr_texts[doc_type] = ocr_result
            except Exception as err:
                results.append({"type": doc_type, "status": "error", "message": str(err)})

            try:
                structured = extract_structure_data_from_text(
                    ocr_texts, openai_api=current_user.openai_api
                )
                record = Ocr.create(
                    user_id=current_user.id,
                    raw_text=json.dumps(ocr_texts, ensure_ascii=False),
                    **structured,
                    created_at=datetime.now(),
                )

                results.append({"status": "success", "id": record.id})
                return redirect(url_for('show_ocr_list'))
            except Exception as err:
                results.append({"status": "error", "message": str(err)})
        
        if not results:
            return f"エラー: ファイルが選択されていません"
        
        return jsonify(results)
    
@app.route("/ocr_list/", methods=['GET'])
@login_required
def show_ocr_list():
    ocrs = Ocr.get_by_user_id(user_id=current_user.id)
    form = OcrDeleteForm()
    return render_template('ocr_list.html', ocrs=ocrs, form=form)

@app.route("/ocr_list/<int:ocr_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_ocr(ocr_id):
    ocr = Ocr.get_by_id(ocr_id)
    form = OcrEditForm(obj=ocr)
    if not ocr:
        abort(404)
    
    if form.validate_on_submit():
        form.populate_obj(ocr)
        Ocr.update(
            ocr_id=ocr_id,
            user_id=current_user.id,
            new_owner_name=form.new_owner_name.data,
            new_owner_address_main=form.new_owner_address_main.data,
            new_owner_address_street=form.new_owner_address_street.data,
            new_owner_address_number=form.new_owner_address_number.data,
        )
        return redirect(url_for('show_ocr_list'))
    else:
        print(f"{form.errors}")
    return render_template('edit_ocr.html', form=form, ocr=ocr)

@app.route("/ocr_list/<int:ocr_id>/delete", methods=['POST'])
@login_required
def delete_ocr(ocr_id):
    form = OcrDeleteForm()
    if not form.validate_on_submit():
        abort(400)
    ocr = Ocr.get_by_id(ocr_id)
    if not ocr:
        abort(404)
    result = Ocr.delete(ocr_id)
    if not result:
        abort(500)
    return redirect(url_for('show_ocr_list'))