from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    swagger = Swagger(app)
     ## Initialize Config
    app.register_blueprint(home_api, url_prefix='/api')

    app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server".format(**config)


    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)