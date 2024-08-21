""" Run the app """

from app import create_app
from app.schema import manage_db
from app.utils import parse_args


if __name__ == '__main__':
    args = parse_args()
    app = create_app()
    manage_db(app, args)
    app.run(debug=True, host='0.0.0.0')
