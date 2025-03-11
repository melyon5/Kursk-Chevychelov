from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/answer')
def answer():
    data = {
        'title': 'Mars One',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'высшее',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }
    return render_template('auto_answer.html', **data)

@app.route('/auto_answer')
def auto_answer():
    data = {
        'title': 'Mars One',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'высшее',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }
    return render_template('auto_answer.html', **data)

if __name__ == '__main__':
    app.run()
