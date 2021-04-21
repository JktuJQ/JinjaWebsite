from declarations import *
from application import application, redirect, render_template, request, cookie


@application.route('/', methods=["GET"])
def base():
    """Website home page"""

    session = sessions["main_database"]

    services = session.query(Service).all()

    data = {
        "services": []
    }

    for service in services:

        description = session.query(Description).filter(Description.id == service.description_id).first()
        images = session.query(Images).filter(Images.out_id == description.images_id).all()

        service_comments = session.query(Comment)\
            .filter((Comment.service_id == service.id)).all()

        data["services"].append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": {
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in images],
                "description": description.description,
            },
            "average_rating": sum([comment.rating for comment in service_comments]) / len(service_comments)
        })

    return render_template("base.html", data=data, len=len, round=round)


@application.route('/profile/<int:user_id>', methods=["GET"])
def profile(user_id: int):
    return render_template("profile.html")


@application.route('/service/<int:service_id>', methods=["GET"])
def service(service_id: int):
    session = sessions["main_database"]

    service = session.query(Service)\
        .filter(Service.id == service_id).first()

    service_author = session.query(User)\
        .filter(User.id == service.user_id).first()
    service_author_image = session.query(Images)\
        .filter(Images.out_id == service_author.image_id).first()

    service_description = session.query(Description)\
        .filter(Description.id == service.description_id).first()
    service_description_images = session.query(Images)\
        .filter(Images.out_id == service_description.images_id).all()

    service_comments = session.query(Comment, Description)\
        .filter((Comment.service_id == service.id), (Description.id == Comment.description_id)).all()

    data = {
        "service": {
            "author": {
                "id": service_author.id,
                "name": service_author.name,
                "image": str(buffer_image(service_author_image.id, service_author_image.image)) + ".png",
                "phone": service_author.phone,
                "average_rating": 0
            },

            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": {
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in service_description_images],
                "description": service_description.description,
            },
            "comments": []
        }
    }

    average_rating = 0

    for comment, description in service_comments:
        author = session.query(User).filter(User.id == comment.user_id).first()
        author_image = session.query(Images).filter(Images.out_id == author.image_id).first()
        data["service"]["comments"].append({
            "id": comment.id,
            "author": {
                "id": author.id,
                "name": author.name,
                "image": str(buffer_image(author_image.id, author_image.image)) + ".png"
            },
            "description": {
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in session.query(Images).filter(Images.id == description.images_id).all()],
                "description": description.description
            },
            "rating": comment.rating
        })
        average_rating += comment.rating
    data["service"]["author"]["average_rating"] = average_rating / len(data["service"]["comments"])

    return render_template("service.html", data=data)


@application.route('/registration', methods=["GET", "POST"])
def registration():
    """Website registration page"""

    if request.method == "GET":
        return render_template("registration.html")

    elif request.method == "POST":
        phone = request.form.get("phone")
        name = " ".join([request.form.get("surname"), request.form.get("name")])
        password = request.form.get("password")
        image = str(request.files["file"].read())

        try:
            session = sessions["main_database"]
            user = User(phone=phone, password=password, name=name, image=image)
            user_id = user.id
            user_hash = hash((phone, password))
            session.add(user)
            session.commit()
        except Exception:
            # TODO alarm box
            return redirect('/registration')

        cookie["id"] = user_id
        cookie["hash"] = user_hash

        return redirect('/')


@application.route('/create_service', methods=["GET", "POST"])
def create_service():

    if request.method == "GET":
        return render_template("create_service.html")

    elif request.method == "POST":

        title = request.form.get("title")
        image = request.files.get("photo")
        description = request.form.get("description")
        price = request.form.get("price")

        try:

            session = sessions["main_database"]

            user_id = cookie["id"]

            last_out_id = max([image.out_id for image in session.query(Images).all()]) + 1

            image = Images(out_id=last_out_id, image=bytes(image.read()))
            description = Description(description=description, images_id=image.out_id)
            service = Service(user_id=user_id, name=title, description_id=description.id, price=price)

            session.add(image)
            session.add(description)
            session.add(service)

            session.commit()

        except Exception:
            return redirect('/')

        return redirect('/')


@application.route('/comment/<int:service_id>', methods=["GET", "POST"])
def create_comment(service_id: int):

    if request.method == "GET":
        return render_template("create_comment.html")

    elif request.method == "POST":

        impression = request.form.get("impression")
        pluses = request.form.get("pluses")
        minuses = request.form.get("minuses")
        comment = request.form.get("comment")
        rating = request.form.get("rating")

        try:
            session = sessions["main_database"]

            user_id = cookie["id"]

            description = Description(description=delimiter.join((impression, pluses, minuses, comment)))
            comment = Comment(user_id=user_id, service_id=service_id, description_id=description.id, rating=rating)

            session.add(description)
            session.add(comment)

            session.commit()

        except Exception:
            return redirect('/')

        return redirect('/')
