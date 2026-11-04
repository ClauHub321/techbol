from datetime import date
from .extensions import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)

    pedidos = db.relationship(
        "Pedido", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cliente {self.nombre}>"


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    pedidos = db.relationship("Pedido", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    monto = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    producto_id = db.Column(
        db.Integer, db.ForeignKey("productos.id"), nullable=False
    )
    cliente_id = db.Column(
        db.Integer, db.ForeignKey("clientes.id"), nullable=False
    )

    cliente = db.relationship("Cliente", back_populates="pedidos")
    producto = db.relationship("Producto", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido {self.id}>"
