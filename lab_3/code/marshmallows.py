from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.String(required=True)


class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class RecodSchema(Schema):
    id = fields.Str(dump_only=True)
    userID = fields.Str(required=True)
    categoryID = fields.Str(required=True)
    time = fields.Str(dump_only=True)
    amountOfExpenditure = fields.Str(required=True)