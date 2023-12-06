from flask import Flask, render_template

app = Flask(__name__)

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