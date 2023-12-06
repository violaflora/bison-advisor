from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# change instance_path to the root folder on your machine
app = Flask(__name__, instance_path='/Users/violetedwards/Code/bison-advisor/')
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bison2023'
db = SQLAlchemy(app)

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
    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)