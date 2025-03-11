import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
        return redirect(url_for('gallery'))
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', title='Красная планета', images=images)

if __name__ == '__main__':
    app.run(port=8080)
