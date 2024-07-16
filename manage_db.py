""" Manage Database """

from app import create_app
from app.schema import db

def initialize_database():
    """ Create the database tables """
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    initialize_database()
