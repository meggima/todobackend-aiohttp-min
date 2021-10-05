from aiohttp import web
from aiohttp.web_response import json_response
from database import Tag

class TagsHandler:

    def __init__(self, sessionMaker, converter):
        self.sessionMaker = sessionMaker
        self.converter = converter


    def get_all_tags(self, request):
        with self.sessionMaker() as session:
            allTags = session.query(Tag).all()

            return web.json_response([
                self.converter.mapTag(tag, request) for tag in allTags
            ])


    def remove_all_tags(self, request):
        with self.sessionMaker() as session:
            session.query(Tag).delete()
            session.commit()
            return web.Response(status=204)


    def get_one_tag(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            tag = session.query(Tag).filter_by(tag_id=id).one_or_none()

            if tag == None:
                return web.json_response({'error': 'Tag not found'}, status=404)

            return web.json_response(self.converter.mapTag(tag, request))


    async def create_tag(self, request):
        data = await request.json()

        newTag = Tag()

        self.converter.updateTagFromJson(newTag, data)

        with self.sessionMaker() as session:
            session.add(newTag)
            session.commit()

            return web.Response(
                headers={'Location': self.converter.mapTag(newTag, request)['url']},
                status=303
            )


    async def update_tag(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            tag = session.query(Tag).filter_by(tag_id=id).one_or_none()

            if tag == None:
                return web.json_response({'error': 'Tag not found'}, status=404)

            data = await request.json()

            self.converter.updateTagFromJson(tag, data)

            session.add(tag)
            session.commit()

            return web.json_response(self.converter.mapTag(tag, request))


    async def remove_tag(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            tag = session.query(Tag).filter_by(tag_id=id).one_or_none()

            if tag == None:
                return web.json_response({'error': 'Tag not found'})

            session.delete(tag)
            session.commit()

            return web.Response(status=204)


    async def get_one_tag_todos(self, request):
        id = int(request.match_info['id'])

        with self.sessionMaker() as session:
            tag = session.query(Tag).filter_by(tag_id=id).one_or_none()

            if tag == None:
                return web.json_response({'error': 'Tag not found'})

            return json_response([
                self.converter.mapTaskWithoutTags(task, request) for task in tag.tasks
            ])