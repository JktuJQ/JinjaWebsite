from typing import *
import io


T = TypeVar("T")


# database
db_files = [r"data\databases\main_database.sqlite"]

from data import db_session
db_session.global_init(db_files)
from data.db_session import sessions
from data.models import *
