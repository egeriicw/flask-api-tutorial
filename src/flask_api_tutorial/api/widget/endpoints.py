"""API endpoint definitions for /widgets namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.flask_api_tutorial.api.widgets.dto import create_widget_reqparser
from src.flask_api_tutorial.api.widgets.business import create_widget


widgets_ns = Namespace(name="widgets", validate=True)


@widgets_ns.route("", endpoint="widget_list")
@widgets_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@widgets_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@widgets_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class WidgetList(Resource):
    """Handles HTTP requests to URL: /widgets."""

    @widgets_ns.doc(security="Bearer")
    @widgets_ns.response(int(HTTPStatus.CREATED), "Added new widget.")
    @widgets_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @widgets_ns.response(int(HTTPStatus.CONFLICT), "Widget name already exists.")
    @widgets_ns.expect(create_widget_reqparser)
    def post(self):
        """Create a widget."""
        widget_dict = create_widget_reqparser.parse_args()
        return create_widget(widget_dict)
