""" Boookmarks API """

import uuid

from flask import jsonify
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args, parser, abort
from sqlalchemy.exc import IntegrityError

from app.schema import db, Bookmarks, BookmarksSchema

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

bookmarks_json_args = {
    'url': fields.String(required=True)
}
bookmarks_query_args = {
    'url': fields.String(required=False)
}

class BookmarksResource(Resource):
    """ Bookmarks Resource """

    @use_args(bookmarks_query_args, location="query")
    def get(self, args):
        """ Get bookmarks """

        if 'url' in args:
            url_bms = Bookmarks.query.filter_by(url=args['url'])
            return bookmarks_schema.dump(url_bms)
        all_bookmarks = Bookmarks.query.all()
        return bookmarks_schema.dump(all_bookmarks)

    @use_args(bookmarks_json_args, location="json")
    def post(self, args):
        """ Post bookmark """

        bm_id = uuid.uuid4()
        bm_id = str(bm_id)
        bookmark = Bookmarks(
            id=bm_id,
            url=args['url']
        )
        db.session.add(bookmark)
        try:
            db.session.commit()
        except IntegrityError:
            return f"Bad Request: IntegrityError: Bookmark {args['url']} may already exist.", 400
        return f"{bm_id}"


class BookmarkResource(Resource):
    """ Bookmark Resource """

    def get(self, bookmark_id):
        """ Get bookmark """

        bookmark = Bookmarks.query.get_or_404(bookmark_id)
        return bookmark_schema.dump(bookmark)

    def delete(self, bookmark_id):
        """ Delete bookmark """

        bookmark = Bookmarks.query.get_or_404(bookmark_id)
        db.session.delete(bookmark)
        db.session.commit()
        return '', 204


class TestResource(Resource):
    """ Healthcheck Resource """

    def get(self):
        """ Healthcheck endpoint """

        output = { "msg": "This is the test endpoint" }
        return jsonify(output)


# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=err.messages['json'])
