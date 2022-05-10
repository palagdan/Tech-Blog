from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort, request

from blog.posts.forms import PostForm
from blog.models import Post
from blog import db
from flask_login import login_required, current_user

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created', 'success')
        post = Post(title=form.title.data, content=form.content.data, owner=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.article_page'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post1 = Post.query.get_or_404(post_id)
    if post1.author != current_user:
        abort(403)

    db.session.delete(post1)
    db.session.commit()
    flash('You post has been deleted', 'success')

    return redirect(url_for('main.article_page'))
