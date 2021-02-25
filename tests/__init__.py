from aiohttp.test_utils import AioHTTPTestCase
from cars_app.main import init
from cars_app.config import TestConfig


class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return init(TestConfig())

    async def tearDownAsync(self):
        await self.app['db'].client.drop_database(self.app['db'])
