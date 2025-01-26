from marshmallow import Schema, fields, validate, ValidationError

class CheckAvailabilitySchema(Schema):
    date = fields.Str(required=True)
    time = fields.Str(required=True)
    vehicle_type = fields.Str(required=True)

class BookSlotSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email())
    slot_id = fields.Str(required=True)
    date = fields.Str(required=True)
    time = fields.Str(required=True)

class ProcessPaymentSchema(Schema):
    booking_id = fields.Int(required=True)
    card_number = fields.Str(required=True, validate=validate.Length(min=16, max=16))
    expiry = fields.Str(required=True, validate=validate.Length(min=5, max=5))
    cvv = fields.Str(required=True, validate=validate.Length(min=3, max=3))