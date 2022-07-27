from flask_restful import Resource, reqparse

from app.schema import db, ma, Bookmarks, BookmarksSchema
import uuid

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

bm_parser = reqparse.RequestParser()
bm_parser.add_argument('url')
bm_args = bm_parser.parse_args()

class BookmarksResource(Resource):
    def get(self):
        all_bookmarks = Bookmarks.query.all()
        return bookmarks_schema.dump(all_bookmarks)

    def post(self):
        bookmark = Bookmarks(
            id=uuid.uuid4(),
            url=bm_args['url']
        )
        db.session.add(bookmark)
        db.session.commit()
        return "post"

class BookmarkResource(Resource):
    def get(self, bookmark_id):
        returned_bookmark = Bookmarks.query.get_or_404(bookmark_id)
        return bookmark_schema.dump(returned_bookmark)
