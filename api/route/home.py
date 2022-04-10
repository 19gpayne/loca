import math
from flask import Blueprint, request
from redis_init import redis_client
import uuid

home_api = Blueprint('api', __name__)

@home_api.route('/')
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    return "Welcome to loca!", 200

@home_api.route('/get_monument', methods=['GET'])
def get_monument():
    """
    Gets a monument with the given ID
    Request format: ?id="monument id"
    """
    monument_id = request.args['id']
    return redis_client.get(monument_id), 200

@home_api.route('/add_monument', methods=['POST'])
def add_monument():
    """
    Adds a monument with the given description
    JSON format: { lat: <lat>, lon: <lon>, title: "title", description: "description" }
    """
    req = request.get_json()

    # TODO call Nicholas's Magic Library

    description = {
        "lat" : req['lat'],
        "lon" : req['lon'],
        "title": req['title'],
        "description": req['description']
    }
    redis_client.set(str(uuid.uuid4()), description), 200

@home_api.route('/find_monument', methods=['POST'])
def find_monument():
    """
    Find a monument given the picture, latitude, and longitude
    Request format: ?lat=<lat> & lon=<lon>
    """
    req = request.get_json()
    user_loc = (float(request.args['lat']), float(request.args['lon']))

    # TODO call Nicholas's Magic Library

    match_ids = []
    closest_monument = None
    closest_monument_dist = None

    for id in match_ids:
        monument = redis_client.get(id)
        monument_dist = math.dist(user_loc, (float(monument['lat']) , float(monument['lon'])))
        if (closest_monument == None or monument_dist < closest_monument_dist):
            closest_monument_dist = monument_dist
            closest_monument = monument

    return closest_monument, 200

@home_api.route('/edit_description', methods=['POST'])
def edit_description():
    """
    Edits the description of an object
    JSON request format {id: "id", desc: "desc", date: yyyy/mm/dd}
    """
    req = request.get_json()
    description = redis_client.get(req['id'])
    description['description'] = req['description']
    description['datetime'] = req['datetime']
    redis_client.set(req['id'], description), 200