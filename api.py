import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from sqlalchemy.sql import func
from random import Random

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'cockroachdb://root@haproxy:26257/tagger_db?sslmode=disable'
db = SQLAlchemy(app)
api = Api(app)

class TestTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Test Table {self.id}>'



class HelloWorld(Resource):
    def get(self):
        rand_int = int(Random().random() * 10000)
        test_col = TestTable(id=rand_int)
        db.session.add(test_col)
        db.session.commit()
        returned_col = TestTable.query.get_or_404(rand_int)
        print(f'returned_col: {returned_col}')
        return {
            'hello': 'world',
            'id': returned_col.id,
            'created_at': returned_col.created_at
        }

api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
