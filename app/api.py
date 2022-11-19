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
        try:
            db.session.add(bookmark)
            db.session.commit()
        except IntegrityError:
            return 'Bad Request: IntegrityError: Bookmark {} may already exist.'.format(args['url']), 400
        except:
            return 'Bad Request', 400
        return str(bm_id)


class BookmarkResource(Resource):

    def get(self, bookmark_id):
        bookmark = Bookmarks.query.get_or_404(bookmark_id)
        return bookmark_schema.dump(bookmark)

    def delete(self, bookmark_id):
        bookmark = Bookmarks.query.get_or_404(bookmark_id)
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
    print(f"err: {err}")
    print(f"req: {req}")
    print(f"schema: {schema}")
    print(f"error_status_code: {error_status_code}")
    print(f"error_headers: {error_headers}")
    abort(422, str(err))
