from aiohttp import web
from aiohttp.web_response import json_response

from database import Tag, Task

class TasksHandler:

    def __init__(self, sessionMaker, converter):
        self.sessionMaker = sessionMaker
        self.converter = converter

    def get_all_todos(self, request):
        with self.sessionMaker() as session:
            allTasks = session.query(Task).all()

            return web.json_response([
                self.converter.mapTask(task, request) for task in allTasks
            ])

    def remove_all_todos(self, request):
        with self.sessionMaker() as session:
            session.query(Task).delete()
            session.commit()

            return web.Response(status=204)

    def get_one_todo(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Todo not found'}, status=404)

            return web.json_response(self.converter.mapTask(task, request))

    async def create_todo(self, request):
        data = await request.json()

        newTask = Task()

        self.converter.updateTaskFromJson(newTask, data)

        with self.sessionMaker() as session:
            session.add(newTask)
            session.commit()

            return web.Response(
                headers={'Location': self.converter.mapTask(newTask, request)['url']},
                status=303
            )

    async def update_todo(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Todo not found'}, status=404)

            data = await request.json()

            self.converter.updateTaskFromJson(task, data)

            session.add(task)
            session.commit()

            return web.json_response(self.converter.mapTask(task, request))

    def remove_todo(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Todo not found'})

            session.delete(task)
            session.commit()

            return web.Response(status=204)

    async def get_one_todo_alltags(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Task not found'})

            return web.json_response([
                self.converter.mapTag(tag, request) for tag in task.tags
            ])

    async def add_one_todo_tag(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Task not found'})

            data = await request.json()

            if 'id' not in data:
                return web.json_response({'error': 'No tag specified'})

            tag = session.query(Tag).filter_by(tag_id=data['id']).one_or_none()

            if tag == None:
                return web.json_response({'error': 'Tag not found'})

            task.tags.append(tag)

            session.add(task)
            session.commit()

            return web.json_response({'error': 'Tag not found'})

    async def remove_one_todo_tag(self, request):
        id = int(request.match_info['id'])
        tagId = int(request.match_info['tagId'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Task not found'})

            tagToDelete = None
            for tag in task.tags:
                if tag.tag_id == tagId:
                    tagToDelete = tag
                    break

            if tagToDelete == None:
                return web.json_response({'error': 'Tag not found'})

            task.tags.remove(tagToDelete)

            session.add(task)
            session.commit()

            return web.Response(status=204)

    async def remove_one_todo_alltags(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            task = session.query(Task).filter_by(task_id=id).one_or_none()

            if task == None:
                return web.json_response({'error': 'Task not found'})

            task.tags = []

            session.add(task)
            session.commit()

            return web.Response(status=204)