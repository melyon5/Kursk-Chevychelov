from flask_restful import Resource, reqparse, abort
from flask import jsonify
from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument("surname", required=True, type=str)
parser.add_argument("name", required=True, type=str)
parser.add_argument("email", required=True, type=str)
parser.add_argument("password", required=True, type=str)
parser.add_argument("city_from", required=False, type=str)

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({"user": user.to_dict()})
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.surname = args["surname"]
        user.name = args["name"]
        user.email = args["email"]
        user.city_from = args.get("city_from")
        user.set_password(args["password"])
        session.commit()
        return jsonify({"success": "OK"})
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({"success": "OK"})

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({"users": [user.to_dict() for user in users]})
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args["email"]).first():
            abort(400, message="User already exists")
        user = User(
            surname=args["surname"],
            name=args["name"],
            email=args["email"],
            city_from=args.get("city_from")
        )
        user.set_password(args["password"])
        session.add(user)
        session.commit()
        return jsonify({"user_id": user.id})
