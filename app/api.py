from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args, parser, abort

from app.schema import db, ma, Bookmarks, BookmarksSchema
import uuid

from sqlalchemy.exc import IntegrityError

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

bookmarks_json_args = {
    'url': fields.String(required=True)
}
bookmarks_query_args = {
    'url': fields.String(required=False)
}

not_found_msg = ""

class BookmarksResource(Resource):

    @use_args(bookmarks_query_args, location="query")
    def get(self, args):
        if 'url' in args:
            url_bms = Bookmarks.query.filter_by(url=args['url'])
            return bookmarks_schema.dump(url_bms)
        all_bookmarks = Bookmarks.query.all()
        return bookmarks_schema.dump(all_bookmarks)

    @use_args(bookmarks_json_args, location="json")
    def post(self, args):
        bm_id = uuid.uuid4()
        bookmark = Bookmarks(
            id=bm_id,
            url=args['url']
        )
        db.session.add(bookmark)
        try:
            db.session.commit()
        except IntegrityError:
            return 'Bad Request: IntegrityError: Bookmark {} may already exist.'.format(args['url']), 400
        except:
            return 'Bad Request', 400
        return f"{bm_id}"


class BookmarkResource(Resource):

    def __init__(self):
        super().__init__()
        self.not_found_msg = "The requested URL was not found on the server."

    def get(self, bookmark_id):
        fail_msg = f"Failed to get bookmark {bookmark_id}. {self.not_found_msg}"
        bookmark = Bookmarks.query.get_or_404(
            ident=bookmark_id,
            description=jsonify({"message": fail_msg})
        )
        return bookmark_schema.dump(bookmark)

    def delete(self, bookmark_id):
        fail_msg = f"Failed to delete bookmark {bookmark_id}. {self.not_found_msg}"
        bookmark = Bookmarks.query.get_or_404(
            ident=bookmark_id, 
            description=jsonify({"message": fail_msg})
        )
        db.session.delete(bookmark)
        db.session.commit()
        return '', 204


from flask import jsonify
class TestResource(Resource):
    def get(self):
        output = { "msg": "This is the test endpoint" }
        return jsonify(output)


# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=err.messages['json'])
