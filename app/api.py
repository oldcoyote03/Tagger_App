#from flask_restful import Resource, reqparse
from flask_restful import Resource
from flask import request

# testing webargs
from webargs import fields
from webargs.flaskparser import use_args

from app.schema import db, ma, Bookmarks, BookmarksSchema
import uuid

from sqlalchemy.exc import IntegrityError

bookmark_schema = BookmarksSchema()
bookmarks_schema = BookmarksSchema(many=True)

#bm_parser = reqparse.RequestParser()
#bm_parser.add_argument('url')

bookmarks_args = {
    'url': fields.String(required=True)
}

class BookmarksResource(Resource):
    def get(self):
        p_url = request.args.get('url', default="", type=str)
        if p_url:
            url_bms = Bookmarks.query.filter_by(url=p_url)
            return bookmarks_schema.dump(url_bms)
        all_bookmarks = Bookmarks.query.all()
        return bookmarks_schema.dump(all_bookmarks)

    @use_args(bookmarks_args, location="json")
    def post(self, args):
        #args = bm_parser.parse_args()
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
