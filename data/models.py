# Imports
from declarations import *

from .db_session import SqlAlchemyBase


Service = SqlAlchemyBase.classes.service
User = SqlAlchemyBase.classes.user
Comment = SqlAlchemyBase.classes.comment
Status = SqlAlchemyBase.classes.status
