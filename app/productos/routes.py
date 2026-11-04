from flask import render_template, request, redirect, url_for, flash
from . import bp_productos
from ..extensions import db
from ..models import Producto

@bp_productos.get("/")
def listar():
    productos = Producto.query.order_by(Producto.id.desc()).all()
    return render_template("productos/lista.html", productos=productos)

@bp_productos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            precio = float(request.form.get("precio", ""))
            stock = int(request.form.get("stock", ""))
            if not nombre or precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            flash("Ingresa nombre, precio y stock válidos (no negativos).", "warning")
        else:
            db.session.add(Producto(nombre=nombre, precio=precio, stock=stock))
            db.session.commit()
            flash("Producto registrado.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/formulario.html", producto=None)

@bp_productos.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            precio = float(request.form.get("precio", ""))
            stock = int(request.form.get("stock", ""))
            if not nombre or precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            flash("Ingresa datos válidos. Precio y stock no pueden ser negativos.", "warning")
        else:
            producto.nombre, producto.precio, producto.stock = nombre, precio, stock
            db.session.commit()
            flash("Producto actualizado.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/formulario.html", producto=producto)

@bp_productos.post("/eliminar/<int:id>")
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    if producto.pedidos:
        flash("No se puede eliminar: el producto está asociado a pedidos.", "danger")
    else:
        db.session.delete(producto)
        db.session.commit()
        flash("Producto eliminado.", "success")
    return redirect(url_for("productos.listar"))
