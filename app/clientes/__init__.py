from flask import Blueprint

bp_clientes = Blueprint("clientes", __name__, template_folder="../templates")
from . import routes
