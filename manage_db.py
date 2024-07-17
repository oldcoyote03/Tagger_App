""" Manage Database """

import argparse

from app import create_app
from app.schema import db

def initialize_database(app_instance):
    """ Create the database tables """
    with app_instance.app_context():
        db.create_all()

def reset_database(app_instance):
    """ Reset the database tables """
    with app_instance.app_context():
        db.drop_all()
    initialize_database(app_instance)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage the database')
    parser.add_argument('--reset', action='store_true',
                        help='Reset the database')
    args = parser.parse_args()
    app = create_app()
    if not args.reset:
        initialize_database(app)
    else:
        reset_database(app)
