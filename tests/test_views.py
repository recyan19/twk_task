from bson import ObjectId
from aiohttp.test_utils import unittest_run_loop
from cars_app.models import Car
from tests import AppTestCase


class CarListTestCase(AppTestCase):

    @unittest_run_loop
    async def test_list(self):
        car1 = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car1.commit()
        car2 = Car(vin='2', manufacturer='Volvo', model='XC60', color='Blue', prod_year='2020')
        await car2.commit()

        resp = await self.client.get("/")
        assert resp.status == 200
        text = await resp.text()
        assert 'Mercedes' in text
        assert 'Volvo' in text


class CarCreateTestCase(AppTestCase):

    @unittest_run_loop
    async def test_create_item(self):
        data = {
            'vin': '1',
            'manufacturer': 'Mercedes',
            'model': 'S600',
            'color': 'Red',
            'prod_year': '2021'
        }
        resp = await self.client.post("/car/add", data=data)
        assert resp.status == 200

        car = await Car.find_one({})
        assert car.model == data['model']

    @unittest_run_loop
    async def test_bad_request(self):
        car = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car.commit()
        data = {
            'vin': '1',
            'manufacturer': 'Mercedes',
            'model': 'S600',
            'color': 'Red',
            'prod_year': '2021'
        }
        resp = await self.client.post(f"/car/add", data=data)
        text = await resp.text()
        assert 'Error: vin' in text


class CarUpdateTestCase(AppTestCase):

    @unittest_run_loop
    async def test_update(self):
        car = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car.commit()
        data = {
            'vin': '1',
            'manufacturer': 'Mercedes',
            'model': 'S550',
            'color': 'Red',
            'prod_year': '2021'
        }
        resp = await self.client.post(f"/car/{car.id}/update", data=data)
        assert resp.status == 200

        await car.reload()
        assert car.model == data['model']

    @unittest_run_loop
    async def test_not_found(self):
        data = {
            'vin': '1',
            'manufacturer': 'Mercedes',
            'model': 'S550',
            'color': 'Red',
            'prod_year': '2021'
        }
        resp = await self.client.post(f"/car/{ObjectId()}/update", data=data)
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.post(f"/car/{'x'*24}/update", data={})
        assert resp.status == 400

    @unittest_run_loop
    async def test_bad_request(self):
        car = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car.commit()
        data = {
            'model': ''
        }
        resp = await self.client.post(f"/car/{car.id}/update", data=data)
        text = await resp.text()
        assert 'Error: model' in text
        # assert resp.status == 400


class CarDeleteTestCase(AppTestCase):

    @unittest_run_loop
    async def test_delete(self):
        car = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car.commit()
        resp = await self.client.post(f"/car/{car.id}/delete")
        assert resp.status == 200

        assert not (await Car.find_one({'_id': car.id}))

    @unittest_run_loop
    async def test_not_found(self):
        resp = await self.client.post(f"/car/{ObjectId()}/delete")
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.post(f"/car/{'x'*24}/delete")
        assert resp.status == 400


class CarGetTestCase(AppTestCase):

    @unittest_run_loop
    async def test_get(self):
        car = Car(vin='1', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car.commit()
        resp = await self.client.get(f"/car/{car.id}")
        assert resp.status == 200
        data = await resp.text()
        assert 'Mercedes' in data
        assert 'S600' in data

    @unittest_run_loop
    async def test_not_found(self):
        resp = await self.client.get(f"/car/{ObjectId()}")
        assert resp.status == 404

    @unittest_run_loop
    async def test_bad_id(self):
        resp = await self.client.get(f"/car/{'x'*24}")
        assert resp.status == 400


class CarSearchTestCase(AppTestCase):

    async def create_cars(self):
        car1 = Car(vin='1', manufacturer='Mercedes', model='S500', color='Blue', prod_year='2020')
        await car1.commit()
        car2 = Car(vin='2', manufacturer='Mercedes', model='S600', color='Red', prod_year='2021')
        await car2.commit()
        return car1, car2

    @unittest_run_loop
    async def test_search_many_cars(self):
        await self.create_cars()
        resp = await self.client.get('search?q=mercedes')
        assert resp.status == 200

        text = await resp.text()
        assert 'S500' in text
        assert 'S600' in text

    @unittest_run_loop
    async def test_search_one_car(self):
        await self.create_cars()
        resp = await self.client.get('search?q=s600')
        assert resp.status == 200

        text = await resp.text()
        assert 'S500' not in text
        assert 'S600' in text

    @unittest_run_loop
    async def test_search_no_cars(self):
        await self.create_cars()
        resp = await self.client.get('search?q=volvo')
        assert resp.status == 200

        text = await resp.text()
        assert 'Mercedes' not in text
