from declarations import *
from application import application, redirect, render_template, jsonify


@application.route('/', methods=["GET"])
def home():
    """Website home page"""
    return ""


@application.route('/registration', methods=["GET"])
def registration():
    """Website registration page"""
    return open(r"templates\registration.html", encoding="utf8").read()


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
            "comments": {}
        },
    }
    average_rating = 0
    for comment, description in service_comments:
        print(description)
        author = session.query(User).filter(User.id == comment.user_id).first()
        data["service"]["comments"][comment.id] = {
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
        }
        average_rating += comment.rating
    data["service"]["author"]["average_rating"] = average_rating / len(data["service"]["comments"].keys())

    return render_template("service.html", data=jsonify(data))
