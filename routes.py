from declarations import *
from application import application, redirect, render_template, request


@application.route('/', methods=["GET"])
def home():
    """Website home page"""

    session = sessions["main_database"]

    services = session.query(Service).all()

    data = {
        "services": []
    }

    for service in services:

        description = session.query(Description).filter(Description.id == service.description_id).first()
        images = session.query(Images).filter(Images.id == description.images_id).all()

        service_comments = session.query(Comment)\
            .filter((Comment.service_id == service.id)).all()

        data["services"].append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": {
                "images": [image.image for image in images],
                "description": description.description,
            },
            "average_rating": sum([comment.rating for comment in service_comments]) / len(service_comments)
        })

    return render_template("base.html", data=data, len=len, round=round)


@application.route('/registration', methods=["GET", "POST"])
def registration():
    """Website registration page"""

    if request.method == "GET":
        return render_template("rewiew.html")

    elif request.method == "POST":
        pass


@application.route('/register')
def register():
    return "success"


@application.route('/service/<int:service_id>', methods=["GET"])
def service(service_id: int):
    session = sessions["main_database"]

    service = session.query(Service)\
        .filter(Service.id == service_id).first()

    service_author = session.query(User)\
        .filter(User.id == service.user_id).first()

    service_description = session.query(Description)\
        .filter(Description.id == service.description_id).first()
    service_description_images = session.query(Images)\
        .filter(Images.id == service_description.images_id).all()

    service_comments = session.query(Comment, Description)\
        .filter((Comment.service_id == service.id), (Description.id == Comment.description_id)).all()

    data = {
        "service": {
            "author": {
                "id": service_author.id,
                "name": service_author.name,
                "image": service_author.image,
                "phone": service_author.phone,
                "average_rating": 0
            },

            "name": service.name,
            "price": service.price,
            "description": {
                "images": [image.image for image in service_description_images],
                "description": service_description.description,
            },
            "comments": []
        }
    }

    average_rating = 0

    for comment, description in service_comments:
        author = session.query(User).filter(User.id == comment.user_id).first()
        data["service"]["comments"].append({
            "id": comment.id,
            "author": {
                "id": author.id,
                "name": author.name,
                "image": author.image
            },
            "description": {
                "images": [image.image for image in session.query(Images).filter(Images.id == description.images_id).all()],
                "description": description.description
            },
            "rating": comment.rating
        })
        average_rating += comment.rating
    data["service"]["author"]["average_rating"] = average_rating / len(data["service"]["comments"])

    return render_template("service.html", data=data)
