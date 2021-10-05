from aiohttp import web
from database import Tag, Task

class Converter:

    def __init__(self):
        pass

    def updateTaskFromJson(self, task: Task, data):
        if 'title' in data:
            if isinstance(data['title'], str) and len(data['title']):
                task.title = data['title']
            else:
                return web.json_response({'error': '"title" must be a string with at least one character'})

        if 'completed' in data:
            task.completed = bool(data.get('completed'))

        if 'order' in data:
            task.order = int(data.get('order'))

    def updateTagFromJson(self, tag: Tag, data):
        if 'title' in data:
            if isinstance(data['title'], str) and len(data['title']):
                tag.title = data['title']
            else:
                return web.json_response({'error': '"title" must be a string with at least one character'})


    def mapTask(self, task: Task, request):
        return {
            'id': task.task_id,
            'title': task.title,
            'completed': task.completed,
            'order': task.order,
            'url': request.scheme + '://' + request.host + str(request.app.router['one_todo'].url_for(id=str(task.task_id))),
            'tags': [self.mapTagWithoutTodos(tag, request) for tag in task.tags]
        }

    def mapTaskWithoutTags(self, task: Task, request):
        return {
            'id': task.task_id,
            'title': task.title,
            'completed': task.completed,
            'order': task.order,
            'url': request.scheme + '://' + request.host + str(request.app.router['one_todo'].url_for(id=str(task.task_id)))
        }

    def mapTag(self, tag: Tag, request):
        return {
            'id': tag.tag_id,
            'title': tag.title,
            'url': request.scheme + '://' + request.host + str(request.app.router['one_tag'].url_for(id=str(tag.tag_id))),
            'todos': [self.mapTaskWithoutTags(task, request) for task in tag.tasks]
        }

    def mapTagWithoutTodos(self, tag: Tag, request, ):
        return {
            'id': tag.tag_id,
            'title': tag.title,
            'url': request.scheme + '://' + request.host + str(request.app.router['one_tag'].url_for(id=str(tag.tag_id)))
        }