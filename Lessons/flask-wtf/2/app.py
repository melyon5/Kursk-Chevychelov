from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    t = request.args.get('title', 'Заготовка')
    return render_template('base.html', title=t)

@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof.lower() or 'строитель' in prof.lower():
        h = 'Инженерные тренажёры'
        img = url_for('static', filename='engineer.png')
    else:
        h = 'Научные симуляторы'
        img = url_for('static', filename='scientist.png')
    return render_template('training.html', title='Mars One', heading=h, image_url=img)

if __name__ == '__main__':
    app.run()
