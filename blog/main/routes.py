from flask import Blueprint

from flask import Flask, render_template, request

from blog.models import User, Post

from flask_login import  login_required


main = Blueprint('main', __name__)


@main.route('/articles')
@login_required
def article_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('articles.html', posts=posts)


@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')

@main.route('/pythonrepl')
def python_repl():
    return render_template('python_repl/python_repl.html')