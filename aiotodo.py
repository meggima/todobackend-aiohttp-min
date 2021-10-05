import logging
from aiohttp import web
import aiohttp_cors
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from conversion import Converter
from tags import TagsHandler
from tasks import TasksHandler

def initializeDatabase():
    engine = create_engine(f"sqlite:///tasks.db")
    sessionMaker = sessionmaker()
    sessionMaker.configure(bind=engine)
    return sessionMaker

def start():
    sessionMaker = initializeDatabase()
    converter = Converter()
    tasksHandler = TasksHandler(sessionMaker, converter)
    tagsHandler = TagsHandler(sessionMaker, converter)

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

    cors.add(app.router.add_get('/todos/', tasksHandler.get_all_todos, name='all_todos'))
    cors.add(app.router.add_delete('/todos/', tasksHandler.remove_all_todos, name='remove_todos'))
    cors.add(app.router.add_post('/todos/', tasksHandler.create_todo, name='create_todo'))
    cors.add(app.router.add_get('/todos/{id:\d+}', tasksHandler.get_one_todo, name='one_todo'))
    cors.add(app.router.add_patch('/todos/{id:\d+}', tasksHandler.update_todo, name='update_todo'))
    cors.add(app.router.add_delete('/todos/{id:\d+}', tasksHandler.remove_todo, name='remove_todo'))
    cors.add(app.router.add_get('/todos/{id:\d+}/tags/', tasksHandler.get_one_todo_alltags, name='one_todo_tags'))
    cors.add(app.router.add_post('/todos/{id:\d+}/tags/', tasksHandler.add_one_todo_tag, name='add_one_todo_tag'))
    cors.add(app.router.add_delete('/todos/{id:\d+}/tags/{tagId:\d+}', tasksHandler.remove_one_todo_tag, name='remove_one_todo_tag'))
    cors.add(app.router.add_delete('/todos/{id:\d+}/tags/', tasksHandler.remove_one_todo_alltags, name='remove_one_todo_alltags'))
    cors.add(app.router.add_get('/tags/', tagsHandler.get_all_tags, name='all_tags'))
    cors.add(app.router.add_delete('/tags/', tagsHandler.remove_all_tags, name='remove_tags'))
    cors.add(app.router.add_post('/tags/', tagsHandler.create_tag, name='create_tag'))
    cors.add(app.router.add_get('/tags/{id:\d+}', tagsHandler.get_one_tag, name='one_tag'))
    cors.add(app.router.add_patch('/tags/{id:\d+}', tagsHandler.update_tag, name='update_tag'))
    cors.add(app.router.add_delete('/tags/{id:\d+}', tagsHandler.remove_tag, name='remove_tag'))
    cors.add(app.router.add_get('/tags/{id:\d+}/todos/', tagsHandler.get_one_tag_todos, name='get_one_tag_todos'))

    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=8080)

if __name__ == '__main__':
    start()