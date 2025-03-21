from flask_restful import Resource, reqparse, abort
from flask import jsonify
from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument("job_title", required=True, type=str)
parser.add_argument("work_size", required=True, type=int)
parser.add_argument("collaborators", required=True, type=str)
parser.add_argument("is_finished", required=True, type=bool)
parser.add_argument("team_leader", required=True, type=int)

def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({"job": job.to_dict()})
    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        job.job_title = args["job_title"]
        job.work_size = args["work_size"]
        job.collaborators = args["collaborators"]
        job.is_finished = args["is_finished"]
        job.team_leader = args["team_leader"]
        session.commit()
        return jsonify({"success": "OK"})
    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({"success": "OK"})

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({"jobs": [job.to_dict() for job in jobs]})
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job_title=args["job_title"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            is_finished=args["is_finished"],
            team_leader=args["team_leader"]
        )
        session.add(job)
        session.commit()
        return jsonify({"job_id": job.id})
