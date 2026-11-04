from flask import Blueprint

bp_productos = Blueprint("productos", __name__, template_folder="../templates")
from . import routes
