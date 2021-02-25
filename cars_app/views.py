import logging

import aiohttp_jinja2
from bson import ObjectId
from bson.objectid import InvalidId
from umongo import ValidationError
from aiohttp.web_exceptions import HTTPBadRequest

from cars_app import services
from cars_app import schemas
from cars_app.utils import redirect


logger = logging.getLogger(__name__)


class SiteHandler:

    @staticmethod
    def validate_object_id(object_id):
        try:
            object_id = ObjectId(object_id)
        except InvalidId:
            logger.error(f'invalid id {object_id}')
            raise HTTPBadRequest(reason='Invalid id.')
        return object_id

    @staticmethod
    def validate_form_data(data):
        data = {k: v for k, v in data.items() if v}
        return data

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        cars = await services.find_cars()
        cars = [car.dump() async for car in cars]
        return {'cars': cars}

    @aiohttp_jinja2.template('car_detail.html')
    async def get_car(self, request):
        car_id = self.validate_object_id(request.match_info['car_id'])
        car = await services.get_car(car_id)
        return {'car': car.dump()}

    @aiohttp_jinja2.template('add_car.html')
    async def add_car(self, request):
        try:
            schema = schemas.CarSchema()
            valid_data = self.validate_form_data(await request.post())
            data = schema.load(valid_data)
            car = await services.create_car(data)
            return redirect(request, 'get_car', car_id=str(car.id))
        except ValidationError as error:
            logger.error('validation error', extra={'errors': error.messages})
            return {'errors': error.messages}

    @aiohttp_jinja2.template('add_car.html')
    async def add_car_page(self, request):
        return {'errors': None}

    @aiohttp_jinja2.template('car_detail.html')
    async def update_car(self, request):
        car_id = self.validate_object_id(request.match_info['car_id'])
        try:
            schema = schemas.UpdateCarSchema()
            valid_data = self.validate_form_data(await request.post())
            data = schema.load(valid_data)
            car = await services.update_car(car_id, data)
            return redirect(request, 'get_car', car_id=str(car.id))

        except ValidationError as error:
            logger.error('validation error', extra={'errors': error.messages})
            car = await services.get_car(car_id)
            return {'errors': error.messages, 'car': car.dump()}

    async def delete_car(self, request):
        car_id = self.validate_object_id(request.match_info['car_id'])
        await services.delete_car(car_id)
        return redirect(request, 'index')

    @aiohttp_jinja2.template('cars_search.html')
    async def search_cars(self, request):
        query = request.query['q']
        cars = await services.search_cars(query)
        cars = [car.dump() async for car in cars]
        return {'cars': cars}
