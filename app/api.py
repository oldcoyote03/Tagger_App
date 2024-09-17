"""
### Generic API
* The API classes have an instance attribute ``service``
* The API classes require the ``service`` to have the following attributes
  * ``model``: SQLAlchemy model
  * ``schema``: Marshmallow schema
  * ``schema_list``: Marshmallow schema for many records
  * ``query_args``: Webargs URI query arguments
  * ``json_args``: Webargs JSON payload arguments

"""

import logging
from functools import wraps
from flask import abort as flask_abort, Response
from flask.views import MethodView
from webargs.flaskparser import use_args, parser, abort as webargs_abort
from sqlalchemy.exc import IntegrityError
from app.services import SqlaNotFound


log = logging.getLogger(__name__)

def register_api(app, service):
    """ Register the API """
    name = service.get_name()
    item = ItemAPI.as_view(f"{name}-item", service)
    group = GroupAPI.as_view(f"{name}-group", service)
    app.add_url_rule(f"/{name}/<item_id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)

def register_healthcheck(app):
    """ Register the healthcheck endpoint """
    view = HealthcheckView.as_view("healthcheck")
    app.add_url_rule("/healthcheck", view_func=view)

def use_args_wrapper(view_method, location):
    """ use_args wrapper """
    @wraps(view_method)
    def wrapper(*args, **kwargs):
        self = args[0]
        schema = getattr(self.service, f"{location}_args")
        return use_args(schema, location=location)(view_method)(*args, **kwargs)
    return wrapper

def use_args_json(view_method):
    """ use_args wrapper for JSON args """
    return use_args_wrapper(view_method, "json")

def use_args_query(view_method):
    """ use_args wrapper for query args """
    return use_args_wrapper(view_method, "query")


class ItemAPI(MethodView):
    """ Item API """

    def __init__(self, service):
        self.service = service

    def get(self, item_id):
        """ Get item """
        log.info(f"GET /{self.service.get_name()}/{item_id}")
        sqla_resp = self.service.get(item_id)
        if not sqla_resp:
            flask_abort(Response(f"{self.service.get_name()} {item_id} not found", 404))
        return sqla_resp

    def delete(self, item_id):
        """ Delete item """
        log.info(f"DELETE /{self.service.get_name()}/{item_id}")
        try:
            self.service.delete(item_id)
        except SqlaNotFound:
            flask_abort(Response(f"{self.service.get_name()} {item_id} not found", 404))
        return Response("", 204)


class GroupAPI(MethodView):
    """ Group API """

    def __init__(self, service):
        self.service = service

    @use_args_query
    def get(self, args):
        """ Get group """
        log.info(f"GET /{self.service.get_name()} with filter: {args}")
        return self.service.get_all(**args)

    @use_args_json
    def post(self, args):
        """ Post item """
        log.info(f"POST /{self.service.get_name()} with payload: {args}")
        item = self.service.model(**args)
        try:
            self.service.add(item)
        except IntegrityError as ie:
            flask_abort(Response(f"Add {self.service.get_name()} error: {ie.orig}", 400))
        return Response(str(self.service.get_all(**args)[0].get("id")), 200)


class HealthcheckView(MethodView):
    """ Healthcheck View """

    def get(self):
        """ Healthcheck endpoint """
        return Response("OK", 200)


@parser.error_handler
def handle_request_parsing_error(err):
    """ 
    webargs error handler to returna JSON error response to the client.
    other args: req, schema, error_status_code, error_headers
    """
    webargs_abort(422, errors=err.messages.get("json"))
