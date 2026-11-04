from datetime import date
from flask import render_template, request, redirect, url_for, flash
from . import bp_pedidos
from ..extensions import db
from ..models import Pedido, Cliente, Producto

@bp_pedidos.get("/")
def listar():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    return render_template("pedidos/lista.html", pedidos=pedidos)

@bp_pedidos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    if request.method == "POST":
        try:
            cliente = db.session.get(Cliente, int(request.form["cliente_id"]))
            producto = db.session.get(Producto, int(request.form["producto_id"]))
            cantidad = int(request.form["cantidad"])
            fecha = date.fromisoformat(request.form["fecha"])
            if cliente is None or producto is None or cantidad <= 0:
                raise ValueError
            if producto.stock < cantidad:
                flash("Stock insuficiente para la cantidad solicitada.", "danger")
            else:
                pedido = Pedido(
                    cliente=cliente, producto=producto, cantidad=cantidad,
                    fecha=fecha, monto=producto.precio * cantidad
                )
                producto.stock -= cantidad
                db.session.add(pedido)
                db.session.commit()
                flash("Pedido registrado y stock actualizado.", "success")
                return redirect(url_for("pedidos.listar"))
        except (KeyError, TypeError, ValueError):
            flash("Verifica los datos del pedido.", "warning")
    return render_template(
        "pedidos/formulario.html", pedido=None, clientes=clientes,
        productos=productos, fecha_hoy=date.today().isoformat()
    )

@bp_pedidos.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pedido = Pedido.query.get_or_404(id)
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    if request.method == "POST":
        try:
            cliente = db.session.get(Cliente, int(request.form["cliente_id"]))
            producto = db.session.get(Producto, int(request.form["producto_id"]))
            cantidad = int(request.form["cantidad"])
            fecha = date.fromisoformat(request.form["fecha"])
            if cliente is None or producto is None or cantidad <= 0:
                raise ValueError

            # Reintegrar temporalmente el stock del pedido anterior.
            stock_disponible = producto.stock
            if producto.id == pedido.producto_id:
                stock_disponible += pedido.cantidad
            if stock_disponible < cantidad:
                flash("Stock insuficiente para actualizar el pedido.", "danger")
            else:
                pedido.producto.stock += pedido.cantidad
                producto.stock -= cantidad
                pedido.cliente = cliente
                pedido.producto = producto
                pedido.cantidad = cantidad
                pedido.fecha = fecha
                pedido.monto = producto.precio * cantidad
                db.session.commit()
                flash("Pedido actualizado y stock ajustado.", "success")
                return redirect(url_for("pedidos.listar"))
        except (KeyError, TypeError, ValueError):
            flash("Verifica los datos del pedido.", "warning")
    return render_template(
        "pedidos/formulario.html", pedido=pedido, clientes=clientes,
        productos=productos, fecha_hoy=date.today().isoformat()
    )

@bp_pedidos.post("/eliminar/<int:id>")
def eliminar(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.producto.stock += pedido.cantidad
    db.session.delete(pedido)
    db.session.commit()
    flash("Pedido eliminado y stock devuelto.", "success")
    return redirect(url_for("pedidos.listar"))
