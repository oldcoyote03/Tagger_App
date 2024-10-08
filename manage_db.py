""" Manage Database """

from app import create_app
from app.utils import parse_args
from app.schema import manage_db


if __name__ == '__main__':
    args = parse_args()
    app = create_app(args.env)
    manage_db(app, args)
