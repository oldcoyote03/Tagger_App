""" Run the app """

from app import create_app
from app.utils import parse_args


if __name__ == '__main__':
    args = parse_args()
    app = create_app(args.env)
    app.run(debug=args.debug, host=args.host)
