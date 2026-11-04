import click
from flask.cli import with_appcontext
from .extensions import db
from .models import Cliente, Producto

@click.command("seed")
@with_appcontext
def seed_command():
    
    if Cliente.query.count() == 0:
        db.session.add_all([
            Cliente(nombre="Ana Pérez", telefono="70010001"),
            Cliente(nombre="Luis Flores", telefono="70010002"),
            Cliente(nombre="María Rojas", telefono="70010003"),
        ])

    if Producto.query.count() == 0:
        db.session.add_all([
            Producto(nombre="Teclado", precio=120.00, stock=15),
            Producto(nombre="Mouse", precio=65.00, stock=25),
            Producto(nombre="Monitor", precio=950.00, stock=8),
        ])

    db.session.commit()
    click.echo("Datos de prueba cargados correctamente.")
