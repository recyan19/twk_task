import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks import MotorAsyncIOInstance


logger = logging.getLogger(__name__)
instance = MotorAsyncIOInstance()


async def init_mongo(app, mongodb_uri):
    logger.info(f'init mongo')
    loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(mongodb_uri, io_loop=loop)
    return conn.get_database()


async def setup_mongo(app):
    config = app['config']
    app['db'] = await init_mongo(app, config.MONGODB_URI)
    instance.set_db(app['db'])

    async def close_mongo(app):
        logger.info('close mongo')
        app['db'].client.close()

    app.on_cleanup.append(close_mongo)
