""" Manage Database """

import sys
import argparse
import logging

from sqlalchemy.engine.url import make_url
from sqlalchemy.schema import CreateTable

from app import create_app
from app.schema import db

app = create_app()
logger = logging.getLogger("manage_db")

def view_database_details():
    """ View database details """
    logger.info(f"Dialect: {db.engine.dialect.name}")
    for table_name in db.metadata.tables.keys():
        table = db.metadata.tables.get(table_name)
        logger.info(f"{CreateTable(table).compile(db.engine)}")
        logger.info(f"{table.primary_key}")

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
    with app.app_context():
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_name = make_url(database_uri).database
        logger.info(f"Database Name: {database_name}")
        if args.view:
            logger.info("Displaying database tables...")
            pass
        elif args.reset:
            logger.info("Resetting database tables...")
            db.drop_all()
            db.create_all()
        elif args.remove:
            logger.info("Removing database tables...")
            db.drop_all()
        else:
            logger.info("Initializing database tables...")
            db.create_all()
        view_database_details()
