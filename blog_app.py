from flask import Flask, render_template, abort, request, redirect, url_for, Blueprint
from markupsafe import Markup
import markdown

from blog.database.database import db_session
from blog.database.models import Post

blogapp = Blueprint('blogapp', __name__, template_folder='templates', static_folder='blog/static')

@blogapp.route("/blog")
def blog():
    POSTS = Post.query.all()
    # Pass all posts to the blog template
    return render_template("blog.html", posts=POSTS)

@blogapp.route("/blog/<slug>")
def show_post(slug):
    if slug == "new":
        return redirect(url_for('edit_post', post_id=slug))
    post = Post.query.filter(Post.url == slug).first()
    if post is None:
            abort(404)
    post.content = Markup(markdown.markdown(post.content))
    return render_template("post.html", post=post)

@blogapp.route("/blog/<post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    #if not app.debug:
    #    abort(404)
    post = Post.query.filter(Post.url == post_id).first()
    if post is None:
        if post_id != "new":
            abort(404)
        post = Post("new", "Edit", "2000-0-0", "Edit", "Edit")
    if request.method == "POST":
        if(request.form["slug"] == "new"):
            return
        # Update attributes with submitted form data
        post.title = request.form["title"]
        post.url = request.form["slug"].replace(" ", "-").lower()
        post.date = request.form["date"]
        post.summary = request.form["summary"]
        post.content = request.form["content"]
        print(post_id)
        if post_id == "new":
            db_session.add(post)
        # Save updates to the database
        db_session.commit()

    # GET Request: Render the edit form pre-populated with current post data
    return render_template("edit.html", post=post)