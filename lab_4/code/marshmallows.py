from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=20))
    password = fields.String(required=True, validate=validate.Length(min=10, max=20))


class BankAccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    money = fields.Float(required=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=20))


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    time = fields.Str(dump_only=True)
    amount_of_expenditure = fields.Float(required=True)