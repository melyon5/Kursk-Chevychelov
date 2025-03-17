from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Register Form", form=form, message="Passwords do not match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Register Form", form=form, message="This user already exists")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.hashed_password = generate_password_hash(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")
    return render_template("register.html", title="Register Form", form=form)

def main():
    db_session.global_init("db/blogs.db")
    app.run()

if __name__ == '__main__':
    main()
