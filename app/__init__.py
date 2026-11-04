from flask import Flask, render_template
from config import Config
from .extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    
    from . import models

    from .clientes import bp_clientes
    from .productos import bp_productos
    from .pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix="/clientes")
    app.register_blueprint(bp_productos, url_prefix="/productos")
    app.register_blueprint(bp_pedidos, url_prefix="/pedidos")

    from .cli import seed_command
    app.cli.add_command(seed_command)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app
