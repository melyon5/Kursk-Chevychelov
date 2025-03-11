from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/table')
def table():
    sex = request.args.get('sex', 'male').lower()
    age = request.args.get('age', '21')
    try:
        age_int = int(age)
    except ValueError:
        age_int = 21

    if sex == 'female':
        if age_int < 21:
            color = '#FFC0CB'
        else:
            color = '#FF7F50'
    else:
        if age_int < 21:
            color = '#ADD8E6'
        else:
            color = '#87CEEB'

    if age_int < 21:
        martian_image = url_for('static', filename='images/martian_child.png')
    else:
        martian_image = url_for('static', filename='images/martian_adult.png')

    return render_template('cabin_design.html',
                           title='Mars One',
                           color=color,
                           martian_image=martian_image)

if __name__ == '__main__':
    app.run(port=8080)
