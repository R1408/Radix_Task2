from marshmallow import Schema, fields, validate, validates, post_dump, post_load
from marshmallow.exceptions import ValidationError
import re


class RegisterUserSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=16))

    @validates('email')
    def validate_field_name(self, email):
        if not re.match(r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email):
            raise ValidationError('Please Enter valid Email')


class LoginUserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=16))

    @validates('email')
    def validate_field_name(self, email):
        if not re.match(r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email):
            raise ValidationError('Please Enter valid Email')


class UpdateUserSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)

    @validates('email')
    def validate_field_name(self, email):
        if not re.match(r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email):
            raise ValidationError('Please Enter valid Email')