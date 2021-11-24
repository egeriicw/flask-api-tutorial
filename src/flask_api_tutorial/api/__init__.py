from flask import Blueprint
from flask_restx import Api

from src.flask_api_tutorial.api.auth.endpoints import auth_ns
from src.flask_api_tutorial.api.widgets.endpoints import widgets_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT Authorization",
    description="",
    doc="/ui",
    authorization=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(widgets_ns, path="/widgets")
