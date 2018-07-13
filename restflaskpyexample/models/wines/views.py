from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from models.wines.wine import Wine
import models.wines.errors as WineErrors
import models.users.decorators as user_decorators

__author__ = 'mjd'


wine_blueprint = Blueprint('wines', __name__)

@wine_blueprint.route('/search')
def search_template():
    return render_template('/wines/search.html')

@wine_blueprint.route('/admin/search')
@user_decorators.requires_login #mike added
def admin_search():
    return render_template('/wines/admin_search.html')

@wine_blueprint.route('/search_results', methods=['POST'])
def search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    wine = Wine.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/wines/search_results.html', search_phrase= search_phrase, wine= wine)


@wine_blueprint.route('/admin/search_results', methods=['POST'])
@user_decorators.requires_login #mike added
def admin_search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    wine = Wine.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/wines/admin_search_results.html', search_phrase= search_phrase, wine= wine)

@wine_blueprint.route('/admin/new', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def create_new_wine():
    if request.method == 'GET':
        return render_template('/wines/new_wine.html')
    else:
        name = request.form['name']
        region= request.form['region']
        country = request.form['country']
        vintage= request.form['vintage']
        awards= request.form['awards']
        winery= request.form['winery']
        bottle_size= request.form['bottle_size']
        bottle_per_case= request.form['bottle_per_case']
        tasting_note= request.form['tasting_note']
        cs_price1= request.form['cs_price1']
        cs_price2= request.form['cs_price2']
        cs_price3= request.form['cs_price3']
        bot_price1= request.form['bot_price1']
        bot_price2= request.form['bot_price2']
        bot_price3= request.form['bot_price3']
        bottle_upcharge= request.form['bottle_upcharge']
        is_new= request.form['is_new']
        is_organic= request.form['is_organic']
        is_limited= request.form['is_limited']
        new_label= request.form['new_label']
        out_stock= request.form['out_stock']
        wine_info= request.form['wine_info']
        appellation= request.form['appellation']
        wine_type= request.form['wine_type']
        variety= request.form['variety']
        aging= request.form['aging']
        alcohol= request.form['alcohol']
        img_url= request.form['img_url']


        new_wine = Wine(name, region, awards, winery,
                    bottle_size, bottle_per_case,
                    tasting_note, cs_price1, cs_price2,
                    cs_price3, bot_price1, bot_price2,
                    bot_price3, bottle_upcharge,
                    is_new, is_organic,
                    is_limited,
                    new_label, out_stock, wine_info,
                    country, appellation,
                    wine_type, variety, aging,
                    alcohol, img_url, vintage)
        new_wine.save_to_mongo()

        #return make_response("Thanks", 200)
        #return render_template('search.html')
        return render_template('/wines/added_wine.html')

@wine_blueprint.route('/admin/edit/<string:wine_id>', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def edit_wine(wine_id):
    wine = Wine.from_mongo_id(wine_id)
    if request.method == 'GET':
        
        return render_template('/wines/edit_wine.html', wine_id=wine_id, wine= wine)
    else:
        name = request.form['name']
        region= request.form['region']
        country = request.form['country']
        vintage= request.form['vintage']
        awards= request.form['awards']
        winery= request.form['winery']
        bottle_size= request.form['bottle_size']
        bottle_per_case= request.form['bottle_per_case']
        tasting_note= request.form['tasting_note']
        cs_price1= request.form['cs_price1']
        cs_price2= request.form['cs_price2']
        cs_price3= request.form['cs_price3']
        bot_price1= request.form['bot_price1']
        bot_price2= request.form['bot_price2']
        bot_price3= request.form['bot_price3']
        bottle_upcharge= request.form['bottle_upcharge']
        is_new= request.form['is_new']
        is_organic= request.form['is_organic']
        is_limited= request.form['is_limited']
        new_label= request.form['new_label']
        out_stock= request.form['out_stock']
        wine_info= request.form['wine_info']
        appellation= request.form['appellation']
        wine_type= request.form['wine_type']
        variety= request.form['variety']
        aging= request.form['aging']
        alcohol= request.form['alcohol']
        img_url= request.form['img_url']


        edited_wine = Wine(name, region, awards, winery,
                    bottle_size, bottle_per_case,
                    tasting_note, cs_price1, cs_price2,
                    cs_price3, bot_price1, bot_price2,
                    bot_price3, bottle_upcharge,
                    is_new, is_organic,
                    is_limited,
                    new_label, out_stock, wine_info,
                    country, appellation,
                    wine_type, variety, aging,
                    alcohol, img_url, vintage, wine_id)
        edited_wine.update_to_mongo()

        return render_template('/wines/updated_wine.html')

@wine_blueprint.route('/admin/remove/<string:wine_id>', methods=['GET'])
@user_decorators.requires_login #mike added
def remove_wine(wine_id):
    wine = Wine.remove_from_mongo_id(wine_id)
    #if request.method == 'GET':
        
    return render_template('/wines/deleted_wine.html')
    '''else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))'''

@wine_blueprint.route('/details/<string:wine_id>', methods=['GET'])
def show_wine(wine_id):
    wine = Wine.from_mongo_id(wine_id)
    #if request.method == 'GET':
        
    return render_template('/wines/details.html', wine_id=wine_id, wine= wine)
    '''else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))'''


'''@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts())


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
@user_decorators.requires_login
def check_user_alerts(user_id):
    pass'''
