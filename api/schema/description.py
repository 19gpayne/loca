from flask_marshmallow import Schema
from marshmallow import fields


class DescriptionSchema(Schema):
    description_id = fields.Str()
    monument_id = fields.Str()
    content = fields.Str()
    date_created = fields.Date()
    last_updated = fields.Date()