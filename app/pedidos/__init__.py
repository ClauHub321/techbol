from flask import Blueprint

bp_pedidos = Blueprint("pedidos", __name__, template_folder="../templates")
from . import routes
