import requests
from flask import Flask, render_template
from flask_login import LoginManager
from data import db_session
from data.users import User
from users_api import blueprint as users_api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    r = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}').json()
    if 'error' in r:
        return render_template('users_show.html', user=None, map_url='')
    user_data = r['user']
    city = user_data.get('city_from', '')
    if not city:
        return render_template('users_show.html', user=user_data, map_url='')
    try:
        geo = requests.get('http://geocode-maps.yandex.ru/1.x/', params={'geocode': city, 'format': 'json'}).json()
        coords = geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = coords.split()
        map_url = f'https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z=10&l=sat'
    except:
        map_url = ''
    return render_template('users_show.html', user=user_data, map_url=map_url)

def main():
    db_session.global_init('db/mars.db')
    app.register_blueprint(users_api_blueprint)
    app.run(port=5000, host='127.0.0.1')

if __name__ == '__main__':
    main()
