import sqlalchemy
from .db_session import SqlAlchemyBase

class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    job_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
