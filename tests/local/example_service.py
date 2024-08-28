""" Example servide """

from webargs import fields
from app.schema import db, ma, BaseModel
from app.services import SqlaRunner

class Example(BaseModel):
    """ Example model """
    name = db.Column(db.String, index=True, unique=True, nullable=False)
    flag = db.Column(db.Boolean, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

class ExampleSchema(ma.SQLAlchemyAutoSchema):
    """ Example schema """
    class Meta:
        """ Example model """
        model = Example

class ExampleService(SqlaRunner):
    """ Example service """
    model = Example
    schema = ExampleSchema()
    schema_list = ExampleSchema(many=True)
    query_args = {
        "name": fields.Str(required=False),
        "flag": fields.Bool(required=False),
        "quantity": fields.Int(required=False),
    }
    json_args = {
        "name": fields.Str(required=True),
        "flag": fields.Bool(required=False),
        "quantity": fields.Int(required=False),
    }
