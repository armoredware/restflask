from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from models.posts.post import Post
import models.posts.errors as PostErrors
import models.users.decorators as user_decorators

__author__ = 'mjd'


post_blueprint = Blueprint('posts', __name__)


@post_blueprint.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))
