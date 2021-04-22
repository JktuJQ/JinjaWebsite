import os
from typing import *


delimiter = "{|delimiter|}"


# Image converting
from io import BytesIO
from PIL import Image


def image_to_bytes(image) -> bytes:
    bytearr = BytesIO()
    image.save(bytearr, format="PNG")
    bytearr = bytearr.getvalue()
    return bytearr


def bytes_to_image(bytearr: bytes) -> Image:
    return Image.open(BytesIO(bytearr))


def buffer_image(id: int, bytearr: bytes) -> int:
    image = bytes_to_image(bytearr)
    image.save(f"static/images/{id}.png")
    return id


# database
db_files = [r"data\databases\main_database.sqlite"]

from data import db_session
db_session.global_init(db_files)
from data.db_session import sessions
from data.models import *


# sessions["main_database"].add(Images(id=0, out_id=0, image=image_to_bytes(Image.open("images/0.png"))))
# sessions["main_database"].commit()
# sessions["main_database"].add(Images(id=1, out_id=1, image=image_to_bytes(Image.open("images/1.png"))))
# sessions["main_database"].commit()
# sessions["main_database"].add(Images(id=2, out_id=2, image=image_to_bytes(Image.open("images/2.png"))))
# sessions["main_database"].commit()


# Search
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

schema = Schema(id=ID(stored=True), content=TEXT)
ix = create_in("index", schema)
searcher = ix.searcher()

search_result: List[Dict] = list()


def reload_document(services: List[Service]):
    global ix

    ix = create_in("index", schema)

    with ix.writer() as writer:
        for service in services:
            writer.add_document(id=str(service.id), content=service.name)
    searcher.close()
