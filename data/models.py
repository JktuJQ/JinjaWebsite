# Imports
from declarations import *

from .db_session import databases


# main_database.sqlite
database = databases["main_database"].classes

User = database.user
Service = database.service
Comment = database.create_comment
Description = database.description
Images = database.images
Status = database.status
