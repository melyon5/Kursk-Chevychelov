from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = [
        'инженер-исследователь',
        'пилот',
        'строитель',
        'экзобиолог',
        'врач',
        'инженер по терраформированию',
        'климатолог',
        'специалист по радиационной защите',
        'астрогеолог',
        'гляциолог',
        'инженер жизнеобеспечения',
        'метеоролог',
        'оператор марсохода',
        'киберинженер',
        'штурман',
        'пилот дронов'
    ]
    return render_template('list_prof.html', title='Mars One', list_type=list_type, professions=professions)

if __name__ == '__main__':
    app.run()
