import pathlib

import jinja2
import logging
import aiohttp_jinja2
from aiohttp import web
from cars_app.db import setup_mongo
from cars_app.models import ensure_indexes
from cars_app.config import Config

from cars_app.routes import setup_routes
from cars_app.views import SiteHandler


logger = logging.getLogger(__name__)

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


def setup_jinja(app):
    jinja_env = aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    )


def init(config):
    logger.info(f'init app: {config}')
    app = web.Application()
    app['config'] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(ensure_indexes)
    setup_jinja(app)
    handler = SiteHandler()
    setup_routes(app, handler, PROJECT_ROOT)
    return app


def main():
    config = Config()
    app = init(config)
    web.run_app(app, host=config.HOST, port=config.PORT)


if __name__ == '__main__':
    main()
