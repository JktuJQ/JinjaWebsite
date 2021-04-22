from declarations import *
from application import application, Response, redirect, render_template, request, cookie


@application.route('/', methods=["GET", "POST"])
def base():
    """Website home page"""

    if request.method == "POST" and request.form.get("tel") and request.form.get("password"):
        user = sessions["main_database"].query(User)\
            .filter(User.phone == request.form.get("tel"), User.password == request.form.get("password")).first()
        if user:
            cookie["id"] = user.id
            return redirect('/')

    global searcher

    session = sessions["main_database"]

    services = session.query(Service).all()

    searched = request.form.get("search")
    if searched:
        reload_document(services)

        searcher = ix.searcher()
        query = QueryParser("content", ix.schema).parse(searched)
        search_result = list(searcher.search(query))
        if not search_result:
            services = list(filter(lambda x: searched in x.name, services))
        else:
            services_id = [int(hit["id"]) for hit in search_result]
            services = list(filter(lambda x: x.id in services_id, services))

    data = {
        "services": []
    }

    for service in services:
        description = session.query(Description).filter(Description.id == service.description_id).first()
        images = session.query(Images).filter(Images.out_id == description.images_id).all()

        service_comments = session.query(Comment) \
            .filter((Comment.service_id == service.id)).all()

        data["services"].append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": {
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in images],
                "description": {
                    "comment": description.description
                },
            },
            "average_rating": sum([comment.rating for comment in service_comments]) / len(service_comments)
        })

    return render_template("base.html", data=data, len=len, round=round)


@application.route('/profile/<int:user_id>/', methods=["GET", "POST"])
@application.route('/profile/<int:user_id>/<string:type>', methods=["GET", "POST"])
def profile(user_id: int, type: str = "services"):

    if request.method == "POST" and request.form.get("tel") and request.form.get("password"):
        user = sessions["main_database"].query(User)\
            .filter(User.phone == request.form.get("tel"), User.password == request.form.get("password")).first()
        if user:
            cookie["id"] = user.id
            return redirect('/')

    session = sessions["main_database"]

    user = session.query(User).filter(User.id == user_id).first()
    user_image = session.query(Images).filter(Images.out_id == user.image_id).first()

    services = session.query(Service).filter(Service.user_id == user_id).all()

    data = {
        "registered": cookie.get("id") == user_id,
        "user": {
            "id": user_id,
            "name": user.name,
            "image": str(buffer_image(user_image.id, user_image.image)) + ".png",
            "phone": user.phone,
            "average_rating": 0
        },
        "services": [],
        "comments": []
    }

    for service in services:
        description = session.query(Description).filter(Description.id == service.description_id).first()
        images = session.query(Images).filter(Images.out_id == description.images_id).all()

        service_comments = session.query(Comment, Description) \
            .filter((Comment.service_id == service.id), (Description.id == Comment.description_id)).all()

        data["services"].append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": {
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in images],
                "description": {
                    "comment": description.description
                },
            },
        })

        for comment, description in service_comments:
            author = session.query(User).filter(User.id == comment.user_id).first()
            author_image = session.query(Images).filter(Images.out_id == author.image_id).first()
            data["comments"].append({
                "id": comment.id,
                "author": {
                    "id": author.id,
                    "name": author.name,
                    "image": str(buffer_image(author_image.id, author_image.image)) + ".png"
                },
                "description": {
                    "images": [str(buffer_image(image.id, image.image)) + ".png" for image in
                               session.query(Images).filter(Images.id == description.images_id).all()],
                    "description": {
                        "impression": description.description.split(delimiter)[0],
                        "pluses": description.description.split(delimiter)[1],
                        "minuses": description.description.split(delimiter)[2],
                        "comment": description.description.split(delimiter)[3]
                    }
                },
                "rating": comment.rating
            })
            data["user"]["average_rating"] += comment.rating
    data["user"]["average_rating"] /= len(data["comments"])

    if type == "services":
        return render_template("profile.html", data=data, len=len, round=round)
    elif type == "create_service":
        return redirect('/create_service')
    elif type == "comment":
        return render_template("profile_comment.html", data=data, len=len, round=round)
    elif type == "rating":
        return render_template("profile_rating.html", data=data, len=len, round=round)


@application.route('/service/<int:service_id>', methods=["GET"])
def service(service_id: int):

    if request.method == "POST" and request.form.get("tel") and request.form.get("password"):
        user = sessions["main_database"].query(User)\
            .filter(User.phone == request.form.get("tel"), User.password == request.form.get("password")).first()
        if user:
            cookie["id"] = user.id
            return redirect('/')

    session = sessions["main_database"]

    service = session.query(Service) \
        .filter(Service.id == service_id).first()

    service_author = session.query(User) \
        .filter(User.id == service.user_id).first()
    service_author_image = session.query(Images) \
        .filter(Images.out_id == service_author.image_id).first()

    service_description = session.query(Description) \
        .filter(Description.id == service.description_id).first()
    service_description_images = session.query(Images) \
        .filter(Images.out_id == service_description.images_id).all()

    service_comments = session.query(Comment, Description) \
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
                "description": {
                    "comment": service_description.description
                },
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
                "images": [str(buffer_image(image.id, image.image)) + ".png" for image in
                           session.query(Images).filter(Images.id == description.images_id).all()],
                "description": {
                    "impression": description.description.split(delimiter)[0],
                    "pluses": description.description.split(delimiter)[1],
                    "minuses": description.description.split(delimiter)[2],
                    "comment": description.description.split(delimiter)[3]
                }
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
        image = request.files["file"]

        try:
            session = sessions["main_database"]

            last_out_id = max([user.image_id for user in session.query(User).all()]) + 1
            image = Images(out_id=last_out_id, image=bytes(image.read()))
            user = User(phone=phone, password=password, name=name, image_id=image.out_id)
            user_id = user.id
            user_hash = hash((phone, password))
            session.add(user)
            session.commit()
        except Exception:
            # TODO alarm box
            return redirect('/registration')

        cookie["id"] = user_id

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

            last_out_id = max([user.image_id for user in session.query(User).all()]) + 1

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


@application.route('/create_comment/<int:service_id>', methods=["GET", "POST"])
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