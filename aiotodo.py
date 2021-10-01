import logging
from aiohttp import web
import aiohttp_cors
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from database import Task

engine = create_engine(f"sqlite:///tasks.db")
Session = sessionmaker()

Session.configure(bind=engine)

session = Session()

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'tags': []},
    1: {'title': '?????', 'order': 2, 'completed': False, 'tags': []},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'tags': []}
}

TAGS = {
    0: { 'title': 'Work' },
    1: { 'title': 'Fun' },
    2: { 'title': 'Other' }
}

def get_all_todos(request):
    allTasks = session.query(Task).all()

    return web.json_response([
        mapTask(task, request) for task in allTasks
    ])

def mapTask(task: Task, request):
    return {
        'id': task.task_id,
        'title': task.title,
        'completed': task.completed,
        'order': task.order,
        'url': str(request.app.router['one_todo'].url_for(id=str(task.task_id)))
    }

def remove_all_todos(request):
    session.query(Task).delete()
    return web.Response(status=204)

def get_one_todo(request):
    id = int(request.match_info['id'])

    task = session.query(Task).filter_by(task_id=id).one_or_none()

    if task == None:
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response(mapTask(task, request))


async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    TODOS[new_id] = { **data, 'tags': [] }

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )

async def update_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])

def remove_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)

def get_all_tags(request):
    return web.json_response([
        {'id': key, **todo} for key, todo in TAGS.items()
    ])

def remove_all_tags(request):
    TAGS.clear()
    return web.Response(status=204)

def get_one_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    return web.json_response({'id': id, **TAGS[id]})

async def create_tag(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    new_id = max(TAGS.keys(), default=0) + 1
    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    TAGS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )

async def update_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TAGS[id].update(data)

    return web.json_response(TAGS[id])

def remove_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'})

    del TAGS[id]

    return web.Response(status=204)



app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))
cors.add(app.router.add_get('/tags/', get_all_tags, name='all_tags'))
cors.add(app.router.add_delete('/tags/', remove_all_tags, name='remove_tags'))
cors.add(app.router.add_post('/tags/', create_tag, name='create_tag'))
cors.add(app.router.add_get('/tags/{id:\d+}', get_one_tag, name='one_tag'))
cors.add(app.router.add_patch('/tags/{id:\d+}', update_tag, name='update_tag'))
cors.add(app.router.add_delete('/tags/{id:\d+}', remove_tag, name='remove_tag'))

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8080)
