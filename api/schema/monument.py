from flask_marshmallow import Schema
from marshmallow import fields


class MonumentSchema(Schema):
    id = fields.Str()
    position = fields.Tuple((fields.Float(), fields.Float()))
    title = fields.Str()
    tags = fields.Str()