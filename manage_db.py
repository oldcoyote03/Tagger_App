""" Manage Database """

import sys
import argparse

from sqlalchemy.engine.url import make_url
from sqlalchemy.schema import CreateTable

from app import create_app
from app.schema import db


def view_database_details():
    """ View database details """
    dialect_name = db.engine.dialect.name
    print(f"Dialect : {dialect_name}")

    tables_names = db.metadata.tables.keys()
    print(f"Table Names: {tables_names}")
    for table_name in tables_names:
        table = db.metadata.tables[table_name]
        print(table.name)
        print(CreateTable(table))
        print()

def parse_args():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(description='Manage the database')
    parser.add_argument('--reset', action='store_true',
                        help='Reset the database')
    parser.add_argument('--view', action='store_true',
                        help='View the database tables')
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
        if args.reset:
            print("Resetting database...")
            db.drop_all()
            db.create_all()
        elif args.view:
            print("Viewing database details...")
            view_database_details()
        else:
            print("Initializing database...")
            db.create_all()
