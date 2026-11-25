from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, session
from app import db
from . import post_bp
from .models import Post, Tag
from .forms import PostForm


# 1. Перегляд списку всіх видимих постів
@post_bp.route('/post')
def all_posts():
    stmt = db.select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('posts.html', posts=posts)


# 2. Створення нового поста
@post_bp.route('/post/create', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        selected_tags = (
            db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            if form.tags.data else []
        )
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data or datetime.utcnow(),
            category=form.category.data,
            user_id=form.author_id.data,
            tags=selected_tags
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for('posts.all_posts'))

    return render_template('add_post.html', form=form, title="Створити новий пост")


# 3. Перегляд конкретного поста
@post_bp.route('/post/<int:id>')
def detail_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template('detail_post.html', post=post)


# 4. Редагування поста
@post_bp.route('/post/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)
    if request.method == 'GET':
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        if form.publish_date.data:
            post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template('add_post.html', form=form, title="Редагувати пост")


# 5. Видалення поста
@post_bp.route('/post/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "danger")
        return redirect(url_for('posts.all_posts'))

    return render_template('delete_confirm.html', post=post)
