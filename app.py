from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__, instance_path='/Users/violetedwards/Code/bison-advisor/')
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bison2023'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    # username can be up to 20 characters, must be entered
    username = db.Column(db.String(20), nullable = False)
    # password can be up to 80 characters after hashing, must be entered
    password = db.Column(db.String(80), nullable = False)

@app.route('/')
# https://youtu.be/71EU8gnZqZQ?si=Mwxt6Y7D3TGVfISr
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)