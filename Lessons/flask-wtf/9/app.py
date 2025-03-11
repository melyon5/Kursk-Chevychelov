import json
import random
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars One')

@app.route('/member')
def member():
    with open(os.path.join('templates', 'crew.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    chosen = random.choice(data)
    return render_template('member.html', chosen=chosen, title='Mars One')

if __name__ == '__main__':
    app.run(port=8080)
