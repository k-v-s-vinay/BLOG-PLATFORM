# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SECRET_KEY'] = 'your_secret_key_here'
# db = SQLAlchemy(app)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

# @app.route('/')
# def index():
#     posts = Post.query.order_by(Post.date_created.desc()).all()
#     return render_template('index.html', posts=posts)

# @app.route('/create', methods=['GET', 'POST'])
# def create_post():
#     if request.method == 'POST':
#         title = request.form['title'].strip()
#         content = request.form['content'].strip()
#         if not title:
#             flash('Title is required!', 'danger')
#             return redirect(url_for('create_post'))
#         if not content:
#             flash('Content cannot be empty!', 'danger')
#             return redirect(url_for('create_post'))
#         new_post = Post(title=title, content=content)
#         try:
#             db.session.add(new_post)
#             db.session.commit()
#             flash('Post created successfully!', 'success')
#             return redirect(url_for('index'))
#         except Exception as e:
#             flash(f'Error creating post: {e}', 'danger')
#             return redirect(url_for('create_post'))
#     return render_template('create_post.html')

# @app.route('/post/<int:post_id>')
# def post_detail(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post_detail.html', post=post)

# @app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
# def edit_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if request.method == 'POST':
#         title = request.form['title'].strip()
#         content = request.form['content'].strip()
#         if not title:
#             flash('Title is required!', 'danger')
#             return redirect(url_for('edit_post', post_id=post_id))
#         if not content:
#             flash('Content cannot be empty!', 'danger')
#             return redirect(url_for('edit_post', post_id=post_id))
#         try:
#             post.title = title
#             post.content = content
#             db.session.commit()
#             flash('Post updated successfully!', 'success')
#             return redirect(url_for('post_detail', post_id=post.id))
#         except Exception as e:
#             flash(f'Error updating post: {e}', 'danger')
#             return redirect(url_for('edit_post', post_id=post_id))
#     return render_template('edit_post.html', post=post)

# @app.route('/delete/<int:post_id>')
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     try:
#         db.session.delete(post)
#         db.session.commit()
#         flash('Post deleted successfully!', 'success')
#     except Exception as e:
#         flash(f'Error deleting post: {e}', 'danger')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     with app.app_context():
#         if not os.path.exists('blog.db'):
#             db.create_all()
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash, Markup, escape
from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import Markup, escape
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# -------------------------
# Custom Filter: nl2br
# -------------------------
@app.template_filter('nl2br')
def nl2br(s):
    return Markup('<br>'.join(escape(s).split('\n')))

# -------------------------
# Database Model
# -------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('create_post'))
        if not content:
            flash('Content cannot be empty!', 'danger')
            return redirect(url_for('create_post'))
        new_post = Post(title=title, content=content)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error creating post: {e}', 'danger')
            return redirect(url_for('create_post'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('edit_post', post_id=post_id))
        if not content:
            flash('Content cannot be empty!', 'danger')
            return redirect(url_for('edit_post', post_id=post_id))
        try:
            post.title = title
            post.content = content
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        except Exception as e:
            flash(f'Error updating post: {e}', 'danger')
            return redirect(url_for('edit_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting post: {e}', 'danger')
    return redirect(url_for('index'))

# -------------------------
# DB Init and Run
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('blog.db'):
            db.create_all()
    app.run(debug=True)
