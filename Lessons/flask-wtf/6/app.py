from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/distribution')
def distribution():
    astronauts = [
        'Ридли Скотт',
        'Энди Уир',
        'Марк Уотни',
        'Венката Капур',
        'Тедди Сандерс',
        'Шон Бин'
    ]
    return render_template('distribution.html', title='Mars One', astronauts=astronauts)

if __name__ == '__main__':
    app.run(port=8080)
