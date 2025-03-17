from flask import Flask
from data import db_session
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    db_session.global_init("db/blogs.db")
    session = db_session.create_session()
    job = Jobs(
        team_leader=1,
        job="deployment of residential modules 1 and 2",
        work_size=15,
        collaborators="2, 3",
        start_date=datetime.datetime.now(),
        is_finished=False
    )
    session.add(job)
    session.commit()
    app.run()

if __name__ == '__main__':
    main()
