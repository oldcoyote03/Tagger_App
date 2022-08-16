from flask_restful import Resource, reqparse

from app.schema import db, ma, Bookmarks, BookmarksSchema
import uuid

from sqlalchemy.exc import IntegrityError

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

bm_parser = reqparse.RequestParser()
bm_parser.add_argument('url')

class BookmarksResource(Resource):
    def get(self):
        all_bookmarks = Bookmarks.query.all()
        return bookmarks_schema.dump(all_bookmarks)

    def post(self):
        args = bm_parser.parse_args()
        bookmark = Bookmarks(
            id=uuid.uuid4(),
            url=args['url']
        )
        msg = 'post'
        try:
            db.session.add(bookmark)
            db.session.commit()
        except IntegrityError:
            msg = 'IntegrityError: Bookmark {} may already exist.'.format(args['url'])
        except:
            msg = 'Error'
        return msg


class BookmarkResource(Resource):

    def get(self, bookmark_id):
        bookmark = Bookmarks.query.get_or_404(bookmark_id)
        return bookmark_schema.dump(bookmark)
    
    def delete(self, bookmark_id):
        bookmark = Bookmarks.query.get_or_404(bookmark_id)
        db.session.delete(bookmark)
        db.session.commit()
        return { 'msg': 'delete /{}'.format(bookmark_id), 204 }


from flask import jsonify
class TestResource(Resource):
    def get(self):
        output = { "msg": "This is the test endpoint" }
        return jsonify(output)
