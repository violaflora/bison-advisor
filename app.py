from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_bcrypt import Bcrypt

# TODO: use os to set instance_path
# for now, change instance_path to the root folder on your machine
app = Flask(__name__, instance_path='/Users/violetedwards/Code/bison-advisor/')
bcrypt = Bcrypt(app)
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bison2023'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    # username can be up to 20 characters, must be entered
    username = db.Column(db.String(20), nullable = False, unique = True)
    # password can be up to 80 characters after hashing, must be entered
    password = db.Column(db.String(80), nullable = False)

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min = 4, max = 20)],
        render_kw={"placeholder": "Username"})
    password = PasswordField(
        validators=[InputRequired(), Length(min = 4, max = 20)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min = 4, max = 20)],
        render_kw={"placeholder": "Username"})
    password = PasswordField(
        validators=[InputRequired(), Length(min = 4, max = 20)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

@app.route('/')
# https://youtu.be/71EU8gnZqZQ?si=Mwxt6Y7D3TGVfISr
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # encrypt password
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html', form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# dashboard sub-pages
@app.route('/dash/chat.html', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('/dash/chat.html')

@app.route('/dash/course-info.html', methods=['GET', 'POST'])
@login_required
def courseInfo():
    return render_template('/dash/course-info.html')

@app.route('/dash/form-generator.html', methods=['GET', 'POST'])
@login_required
def formGenerator():
    return render_template('/dash/form-generator.html')

@app.route('/dash/recommendations.html', methods=['GET', 'POST'])
@login_required
def recommendations():
    return render_template('/dash/recommendations.html')

@app.route('/dash/support-resources.html', methods=['GET', 'POST'])
@login_required
def supportResources():
    return render_template('/dash/support-resources.html')

if __name__ == '__main__':
    app.run(debug=True)