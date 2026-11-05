import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from app import products_collection
from .forms import ProductForm

products_bp = Blueprint('products', __name__, template_folder='templates/products')

def save_image(file):
    if file and file.filename:
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext in ['png', 'jpg', 'jpeg']:
            name = f"{uuid.uuid4().hex}.{ext}"
            upload_dir = os.path.join("app", "static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, name))
            return f"uploads/{name}"
    return None

def get_next_id():
    last = products_collection.find_one(sort=[("id", -1)])
    return (last["id"] + 1) if last and "id" in last else 1

@products_bp.route("/")
def products_list():
    products = list(products_collection.find().sort("id", 1))
    return render_template("products.html", products=products)

@products_bp.route("/<int:id>")
def product_detail(id):
    product = products_collection.find_one({"id": id})
    if not product:
        abort(404)
    return render_template("detail_product.html", product=product)

@products_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = {
            "id": get_next_id(),
            "name": form.name.data,
            "content": form.content.data,
            "price": round(form.price.data, 2),
            "category": form.category.data,
            "quantity": form.quantity.data or 0,
            "image": save_image(form.image.data),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        products_collection.insert_one(product)
        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.products_list"))
    return render_template("add_product.html", form=form)

@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def product_edit(id):
    product = products_collection.find_one({"id": id})
    if not product:
        abort(404)

    form = ProductForm(data=product)
    if form.validate_on_submit():
        update_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": round(form.price.data, 2),
            "category": form.category.data,
            "quantity": form.quantity.data or 0,
        }
        new_image = save_image(form.image.data)
        if new_image:
            update_data["image"] = new_image

        products_collection.update_one({"id": id}, {"$set": update_data})
        flash("Товар успішно оновлено!", "success")
        return redirect(url_for("products.product_detail", id=id))

    return render_template("edit_product.html", form=form, product=product)

@products_bp.route("/<int:id>/delete", methods=["POST"])
def product_delete(id):
    products_collection.delete_one({"id": id})
    flash("Товар видалено!", "info")
    return redirect(url_for("products.products_list"))
