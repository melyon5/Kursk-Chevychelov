import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None

def global_init(db_file):
    global __factory
    if __factory:
        return
    engine = sa.create_engine(f'sqlite:///{db_file}?check_same_thread=False')
    __factory = orm.sessionmaker(bind=engine)
    from . import users, jobs
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()
