from typing import *
import io

from data import db_session


T = TypeVar("T")

db_session.global_init()
session = db_session.get_session()
