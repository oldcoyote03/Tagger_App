from flask_restful import Resource
from schema import Bookmarks, BookmarksSchema
import uuid

bookmarks_schema = BookmarksSchema()

class BookmarksResource(Resource):
    def get(self):
        my_uuid = uuid.uuid4()
        bookmark = Bookmarks(id=my_uuid)
        db.session.add(bookmark)
        db.session.commit()
        returned_bookmark = Bookmarks.query.get_or_404(my_uuid)
        dump_bookmark = bookmarks_schema.dump(returned_bookmark)
        return dump_bookmark
