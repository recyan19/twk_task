from marshmallow import Schema
from .models import Car


CarSchema: Schema = Car.schema.as_marshmallow_schema()


class UpdateCarSchema(CarSchema):
    class Meta:
        fields = ['vin', 'manufacturer', 'model', 'color', 'prod_year']
