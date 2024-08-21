""" Boookmarks API """

import uuid
import logging

from flask import jsonify, abort as flask_abort, Response
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args, parser, abort as webargs_abort
from sqlalchemy.exc import IntegrityError

from app.schema import db, Bookmarks, BookmarksSchema
from app.services import BookmarksService, SqlaNotFound


log = logging.getLogger(__name__)

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

        log.info(f"GET /bookmarks with args: {args}")
        if 'url' in args:
            url_bms = Bookmarks.query.filter_by(url=args['url'])
            return bookmarks_schema.dump(url_bms)
        all_bookmarks = Bookmarks.query.all()
        all_bookmarks_dumped = bookmarks_schema.dump(all_bookmarks)
        log.info(f"all_bookmarks_dumped {type(all_bookmarks_dumped)}: {all_bookmarks_dumped}")
        return bookmarks_schema.dump(all_bookmarks)

    @use_args(bookmarks_json_args, location="json")
    def post(self, args):
        """ Post bookmark """

        log.info(f"POST /bookmarks with args: {args}")
        bm_id = uuid.uuid4()
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
        log.info(f"GET /bookmarks/{bookmark_id}")
        sqla_resp = BookmarksService.get(bookmark_id)
        if not sqla_resp:
            flask_abort(Response(f"Bookmark {bookmark_id} not found", 404))
        return jsonify(sqla_resp)

    def delete(self, bookmark_id):
        """ Delete bookmark """
        log.info(f"DELETE /bookmarks/{bookmark_id}")
        try:
            BookmarksService.delete(bookmark_id)
        except SqlaNotFound as e:
            flask_abort(Response(str(e), 404))
        return "", 204


class HealthcheckResource(Resource):
    """ Healthcheck Resource """

    def get(self):
        """ Healthcheck endpoint """
        return Response("OK", 200)


@parser.error_handler
def handle_request_parsing_error(err):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    other args: req, schema, error_status_code, error_headers
    """
    webargs_abort(422, errors=err.messages['json'])
