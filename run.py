import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from src.api import BookmarksResource

app = Flask(__name__)
app.config.from_object("settings")
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

api.add_resource(BookmarksResource, '/bookmarks')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
