from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.categories import Category
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.job_form import JobForm
from forms.department_form import DepartmentForm
import os

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
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message='User exists')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, message='Wrong credentials')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job_title = form.job_title.data
        job.team_leader = current_user.id
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)

@app.route('/editjob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        return redirect('/')
    if job.team_leader != current_user.id and current_user.id != 1:
        return redirect('/')
    if request.method == 'GET':
        form.job_title.data = job.job_title
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job_title = form.job_title.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)

@app.route('/deletejob/<int:id>')
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job and (job.team_leader == current_user.id or current_user.id == 1):
        db_sess.delete(job)
        db_sess.commit()
    return redirect('/')

@app.route('/departments')
@login_required
def list_departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html', departments=departments)

@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Add Department', form=form)

@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if not dep:
        return redirect('/departments')
    if request.method == 'GET':
        form.title.data = dep.title
        form.chief.data = dep.chief
        form.members.data = dep.members
        form.email.data = dep.email
    if form.validate_on_submit():
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Edit Department', form=form)

@app.route('/delete_department/<int:id>')
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    return redirect('/departments')

def main():
    db_session.global_init("db/mars.db")
    app.run()

if __name__ == '__main__':
    main()
