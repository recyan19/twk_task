from aiohttp import web


def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url_for(**kw)
    return web.HTTPFound(location=location)
