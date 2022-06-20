import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.sql import func
from datetime import date

from random import Random

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object("settings")
db = SQLAlchemy(app)
api = Api(app)

class TestTable(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_at = db.Column(
        db.Date, 
        default=func.current_date(type=db.Date,inherit_cache=False)
    )

    def __repr__(self):
        return f'<Test Table {self.id}>'


class HelloWorld(Resource):
    def get(self):
        my_uuid = uuid.uuid4()
        test_col = TestTable(id=my_uuid)
        db.session.add(test_col)
        db.session.commit()
        returned_col = TestTable.query.get_or_404(my_uuid)
        return {
            'hello': 'world',
            'id': f'{returned_col.id}',
            'created_at': f'{returned_col.created_at}'
        }

api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

