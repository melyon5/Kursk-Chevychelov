from flask import Flask, render_template
from flask_restful import Api
from data import db_session
from users_resource import UsersResource, UsersListResource

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
api = Api(app)
db_session.global_init("db/mars.db")
api.add_resource(UsersListResource, "/api/v2/users")
api.add_resource(UsersResource, "/api/v2/users/<int:user_id>")

@app.route("/")
def index():
    return render_template("index.html")

def main():
    app.run(port=5000, host="127.0.0.1")

if __name__ == "__main__":
    main()
