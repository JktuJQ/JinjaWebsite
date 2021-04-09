# Import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.automap as automap


SqlAlchemyBase: automap.AutomapBase = None
current_session: Session = None


def global_init(db_file: str = r"data\databases\main_database.sqlite") -> None:
    global current_session, SqlAlchemyBase

    if current_session:
        return
    if not db_file:
        raise NameError("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file}?check_same_thread=False"

    engine = sa.create_engine(conn_str)

    metadata = sa.MetaData()
    metadata.reflect(engine, only=['user', 'service', 'comment', 'status'])

    SqlAlchemyBase = automap.automap_base(metadata=metadata)
    SqlAlchemyBase.prepare()
    SqlAlchemyBase.metadata.create_all(engine)

    current_session = Session(engine)


def get_session() -> Session:
    global current_session
    return current_session
