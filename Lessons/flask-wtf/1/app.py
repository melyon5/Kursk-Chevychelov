from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    page_title = request.args.get('title', 'Заготовка')
    return render_template('base.html', title=page_title)

if __name__ == '__main__':
    app.run(debug=True)
