""" Example servide """

from sqlalchemy.orm import Mapped, mapped_column
from webargs import fields
from app.schema import db, ma, UniqueText, UuidPk, CurrentDate, BoolNullable, IntNullable
from app.services import SqlaRunner


class Example(db.Model):
    """ Example model """
    name: Mapped[UniqueText]
    flag: Mapped[BoolNullable]
    quantity: Mapped[IntNullable]
    id: Mapped[UuidPk] = mapped_column(init=False)
    created_at: Mapped[CurrentDate] = mapped_column(init=False)

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
