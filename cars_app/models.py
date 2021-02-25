from umongo import Document, fields
from .db import instance


@instance.register
class Car(Document):
    vin = fields.StringField(required=True, unique=True)
    manufacturer = fields.StringField(required=True)
    model = fields.StringField(required=True)
    color = fields.StringField(required=True,)
    prod_year = fields.StringField(required=True)

    class Meta:
        indexes = ['-vin']


async def ensure_indexes(app):
    await Car.ensure_indexes()
