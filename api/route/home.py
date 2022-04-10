import math
from flask import Blueprint, request
from gcloud import (
    upload_images_from_monuments,
    upload_base64_image,
    create_product,
    get_similar_products_file,
)

from redis_init import redis_client
import json
import uuid

home_api = Blueprint("api", __name__)


@home_api.route("/")
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    return "Welcome to loca!", 200


@home_api.route("/get_monument/", methods=["GET"])
def get_monument():
    """
    Gets a monument with the given ID
    Request format: ?id="monument id"
    """
    monument_id = request.args["id"]
    return redis_client.getConnection().get(monument_id), 200


@home_api.route("/add_monument", methods=["POST"])
def add_monument():
    """
    Adds a monument with the given description
    JSON format: { lat: <lat>, lon: <lon>, title: "title", description: "description", image: "b64 image" }
    """
    # req = request.get_json()
    req = json.loads(request.data, strict=False)

    product_id = str(uuid.uuid4())
    uri = req["image"]
    if not uri.startswith("gs"):
        uri = upload_base64_image(uri)

    create_product(product_id, req["title"])

    description = {
        "lat": req["lat"],
        "lon": req["lon"],
        "title": req["title"],
        "description": req["description"],
        "picture": uri,
    }
    redis_client.getConnection().set(str(uuid.uuid4()), description)
    return True, 200


# Credit to cs95 on Stack Overflow
def get_distance(lat_1, lng_1, lat_2, lng_2):
    lng_1, lat_1, lng_2, lat_2 = map(math.radians, [lng_1, lat_1, lng_2, lat_2])
    d_lat = lat_2 - lat_1
    d_lng = lng_2 - lng_1

    temp = (
        math.sin(d_lat / 2) ** 2
        + math.cos(lat_1) * math.cos(lat_2) * math.sin(d_lng / 2) ** 2
    )

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))


@home_api.route("/find_monument", methods=["POST"])
def find_monument():
    """
    Find a monument given the picture, latitude, and longitude
    Request format: ?lat=<lat> & lon=<lon>
    JSON format: { image: <b64 image> }
    """
    req = request.get_json()
    user_loc = (float(request.args["lat"]), float(request.args["lon"]))

    matches = get_similar_products_file(req["image"], None, 5)

    best_monument = None
    best_monument_score = None

    for match in matches:
        product = match.product
        monument = redis_client.getConnection().get(product.name)
        monument_dist = get_distance(
            user_loc[0], user_loc[1], float(monument["lat"]), float(monument["lon"])
        )

        if monument_dist > 1:
            continue

        monument_score = monument_dist * match.score
        if best_monument == None or monument_score < best_monument_score:
            best_monument_score = monument_score
            best_monument = monument

    return best_monument, 200


@home_api.route("/edit_description", methods=["POST"])
def edit_description():
    """
    Edits the description of an object
    JSON request format {id: "id", desc: "desc", date: yyyy/mm/dd}
    """
    req = request.get_json()
    description = redis_client.getConnection().get(req["id"])
    description["description"] = req["description"]
    description["datetime"] = req["datetime"]
    redis_client.getConnection().set(req["id"], description)

    return True, 200
