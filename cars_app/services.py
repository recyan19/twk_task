from datetime import datetime
from aiohttp.web_exceptions import HTTPNotFound
from .models import Car


async def find_cars():
    return Car.find({})


async def search_cars(query):
    cars = Car.find({
        "$or": [
            {'vin': {'$regex': query, '$options': 'i'}},
            {'manufacturer': {'$regex': query, '$options': 'i'}},
            {'model': {'$regex': query, '$options': 'i'}},
            {'color': {'$regex': query, '$options': 'i'}},
            {'prod_year': {'$regex': query, '$options': 'i'}},
        ]
    })
    return cars


async def create_car(data):
    car = Car(**data)
    await car.commit()
    return car


async def get_car(car_id):
    car = await Car.find_one({'_id': car_id})
    if not car:
        raise HTTPNotFound()

    return car


async def update_car(car_id, data):
    car = await get_car(car_id)

    car.update(data)
    car.updated_time = datetime.utcnow()
    await car.commit()

    return car


async def delete_car(car_id):
    car = await get_car(car_id)
    await car.delete()
