from marshmallow import Schema, fields


class EmailRequestSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    message = fields.Str(required=True)
