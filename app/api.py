from flask_restful import Resource

from app.schema import db, ma, Bookmarks, BookmarksSchema
import uuid

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

class BookmarksResource(Resource):
    def get(self):
        all_bookmarks = Bookmarks.all()
        return bookmarks_schema.dump(all_bookmarks)

    def post(self):
        bookmark = Bookmarks(id=uuid.uuid4())
        db.session.add(bookmark)
        db.session.commit()
        return dump_bookmark

class BookmarkResource(Resource):
    def get(self):
        returned_bookmark = Bookmarks.query.get_or_404(my_uuid)
        return bookmark_schema.dump(returned_bookmark)

