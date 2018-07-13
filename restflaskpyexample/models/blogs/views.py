from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from models.blogs.blog import Blog
import models.blogs.errors as BlogErrors
import models.users.decorators as user_decorators

__author__ = 'mjd'


blog_blueprint = Blueprint('blogs', __name__)


@blog_blueprint.route('/blogs/<string:user_id>')
@blog_blueprint.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@blog_blueprint.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))
