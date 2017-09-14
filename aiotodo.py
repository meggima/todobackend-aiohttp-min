from aiohttp import web
import aiohttp_cors

TODOS = [
    {'title': 'build an API', 'order': 1, 'completed': False},
    {'title': '?????', 'order': 2, 'completed': False},
    {'title': 'profit!', 'order': 3, 'completed': False}
]

def get_all_todos(request):
    return web.json_response([
        {'id': idx, **todo} for idx, todo in enumerate(TODOS)
    ])

def remove_all_todos(request):
    TODOS.clear()
    return web.Response(status=204)

def get_one_todo(request):
    id = int(request.match_info['id'])

    if id >= len(TODOS):
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': id, **TODOS[id]})

async def create_todo(request):
    data = await request.json()

    if not 'title' in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    new_id = len(TODOS)
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=new_id)))

    TODOS.append(data)

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )

async def update_todo(request):
    id = int(request.match_info['id'])

    if id >= len(TODOS):
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])

def remove_todo(request):
    id = int(request.match_info['id'])

    if id >= len(TODOS):
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)

def app_factory(args=()):
    app = web.Application()

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
    cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
    cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
    cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
    cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
    cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))
    return app
