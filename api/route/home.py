from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from

from api.model.models import Monument, Description
from api.model.welcome import WelcomeModel
from api.schema.description import DescriptionSchema
from api.schema.monument import MonumentSchema
from api.schema.welcome import WelcomeSchema

home_api = Blueprint('api', __name__)


@home_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': WelcomeSchema
        }
    }
})
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200


@home_api.route('/get_monument', methods='GET')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Gets a monument with the given id',
            'schema': DescriptionSchema
        }
    }
})
def get_monument():
    """
    Gets a monument with the given ID
    Request format: ?id="monument id"
    """
    monument_id = request.args['id']
    monument = Monument.callproc('stpGetMon', [monument_id])
    return MonumentSchema().dump(monument)


@home_api.route('/edit_description', methods='POST')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Updates the description of a monument',
            'schema': DescriptionSchema
        }
    }
})
def edit_description():
    """
    Edits the description of an object
    JSON request format {id: "id", desc: "desc", date: yyyy/mm/dd, }
    """
    req = request.get_json()
    Description.callproc('stpUpdateDescrip', [])