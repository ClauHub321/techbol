from flask import render_template, request, redirect, url_for, flash
from . import bp_clientes
from ..extensions import db
from ..models import Cliente

@bp_clientes.get("/")
def listar():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template("clientes/lista.html", clientes=clientes)

@bp_clientes.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("Completa todos los campos.", "warning")
        else:
            db.session.add(Cliente(nombre=nombre, telefono=telefono))
            db.session.commit()
            flash("Cliente registrado.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/formulario.html", cliente=None)

@bp_clientes.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("Completa todos los campos.", "warning")
        else:
            cliente.nombre, cliente.telefono = nombre, telefono
            db.session.commit()
            flash("Cliente actualizado.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/formulario.html", cliente=cliente)

@bp_clientes.post("/eliminar/<int:id>")
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    if cliente.pedidos:
        flash("No se puede eliminar: el cliente tiene pedidos registrados.", "danger")
    else:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente eliminado.", "success")
    return redirect(url_for("clientes.listar"))
