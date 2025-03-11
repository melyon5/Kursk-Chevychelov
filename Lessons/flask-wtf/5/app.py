from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/login')
def login():
    return render_template('login.html', title='Аварийный доступ')

if __name__ == '__main__':
    app.run(port=8080)
