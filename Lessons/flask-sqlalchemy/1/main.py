from flask import Flask, redirect
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    captain = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org"
    )
    colonist1 = User(
        surname="Miller",
        name="John",
        age=30,
        position="colonist",
        speciality="geologist",
        address="module_2",
        email="john_miller@mars.org"
    )
    colonist2 = User(
        surname="Doe",
        name="Jane",
        age=28,
        position="colonist",
        speciality="botanist",
        address="module_3",
        email="jane_doe@mars.org"
    )
    colonist3 = User(
        surname="Brown",
        name="Alice",
        age=25,
        position="colonist",
        speciality="engineer",
        address="module_4",
        email="alice_brown@mars.org"
    )
    session.add(captain)
    session.add(colonist1)
    session.add(colonist2)
    session.add(colonist3)
    session.commit()
    app.run()

if __name__ == '__main__':
    main()
