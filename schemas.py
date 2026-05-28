from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    phone = fields.Str(load_default="")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CategorySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    description = fields.Str(load_default="")
    image_url = fields.Str(load_default="")


class MenuItemSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    category_id = fields.Int(required=True)
    image_url = fields.Str(load_default="")
    is_available = fields.Bool(load_default=True)
    is_featured = fields.Bool(load_default=False)
    prep_time = fields.Int(load_default=20)
    tags = fields.List(fields.Str(), load_default=list)


class OrderItemSchema(Schema):
    menu_item_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))


class AddressSchema(Schema):
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    line1 = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    zip = fields.Str(required=True)
    instructions = fields.Str(load_default="")