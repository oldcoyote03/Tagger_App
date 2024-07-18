""" Manage Database """

import sys
import argparse

from sqlalchemy.engine.url import make_url
from sqlalchemy.schema import CreateTable

from app import create_app
from app.schema import db


def view_database_details():
    """ View database details """
    print(f"Dialect : {db.engine.dialect.name}")
    for table_name in db.metadata.tables.keys():
        table = db.metadata.tables.get(table_name)
        print(str(CreateTable(table).compile(db.engine)))

def parse_args():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(description='Manage the database')
    parser.add_argument('--view', action='store_true',
                        help='View the database tables')
    parser.add_argument('--reset', action='store_true',
                        help='Reset the database')
    parser.add_argument('--remove', action='store_true',
                        help='Reset the database')
    if len(argparse.Namespace().__dict__) > 1:
        sys.exit(parser.print_usage())
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    app = create_app()
    with app.app_context():
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_name = make_url(database_uri).database
        print(f"Database Name: {database_name}")
        if args.view:
            pass
        elif args.reset:
            print("Resetting database tables...")
            db.drop_all()
            db.create_all()
        elif args.remove:
            print("Removing database tables...")
            db.drop_all()
        else:
            print("Initializing database tables...")
            db.create_all()
        view_database_details()
