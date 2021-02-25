def setup_routes(app, handler, project_root):
    router = app.router
    h = handler
    router.add_get('/', h.index, name='index')
    router.add_post('/car/add', h.add_car, name='add_car')
    router.add_get('/car/add', h.add_car_page, name='add_car_page')
    router.add_get('/car/{car_id}', h.get_car, name='get_car')
    router.add_post('/car/{car_id}/update', h.update_car, name='update_car')
    router.add_post('/car/{car_id}/delete', h.delete_car, name='delete_car')
    router.add_get('/search', h.search_cars, name='search_cars')
    router.add_static('/static/', path=str(project_root / 'static'), name='static')
