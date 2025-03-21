import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None

def global_init(db_file):
    global __factory
    engine = sa.create_engine(f"sqlite:///{db_file}?check_same_thread=False")
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)

def create_session():
    global __factory
    return __factory()
