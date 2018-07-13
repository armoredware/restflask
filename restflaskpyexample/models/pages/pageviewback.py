
@page_blueprint.route('/admin/page_search')
@user_decorators.requires_login #mike added
def admin_search():
    return render_template('/pages/admin_search.html')

@page_blueprint.route('/page_search_results', methods=['POST'])
def search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    page = page.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/pages/search_results.html', search_phrase= search_phrase, page= page)


@page_blueprint.route('/admin/page_search_results', methods=['POST'])
@user_decorators.requires_login #mike added
def admin_search_results():
    search_phrase = request.form['search_phrase']
    search_type = request.form['search_type']
    search_vintage= request.form['search_vintage']
    search_bottle= request.form['search_bottle']
    search_country= request.form['search_country']
    search_case= request.form['search_case']
    
    page = page.from_mongo(search_phrase, search_type, search_vintage, search_bottle, search_country, search_case)
    return render_template('/pages/admin_search_results.html', search_phrase= search_phrase, page= page)

@page_blueprint.route('/admin/new_page', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def create_new_page():
    if request.method == 'GET':
        return render_template('/pages/new_page.html')
    else:
        domain= request.form['domain']
        user_id= request.form['user_id']
        last_mod= request.form['last_mod']
        timestamp= request.form['timestamp']
        page= request.form['user_id']
        url= request.form['url']
        xss= request.form['xss']
        sqli= request.form['sqli']
        sql= request.form['sql']
        csrf= request.form['csrf']
        hash= request.form['hash']
        uptime= request.form['uptime']
        loadspeed= request.form['loadspeed']
        pagecontent= request.form['pagecontent']
        externallinks= request.form['externallinks']
        scripts= request.form['scripts']
        base64= request.form['base64']
        documenttype= request.form['documents']
        virus= request.form['virus']
        malware= request.form['malware']
        reputation= request.form['reputation']
        popups= request.form['popups']
        bruteforce= request.form['bruteforce']
        title= request.form['title']
        redirect= request.form['redirect']
        sensitivedata= request.form['sensitivedata']
        emailaddresses= request.form['emailaddresses']
        adaissues= request.form['adaissues']
        accesscontrol= request.form['accessontrol']
        vulenrability= request.form['vulnerability']
        scanned= request.form['scanned']
        
        
        new_page = Page(domain, user_id, last_mod, timestamp,
                        url,
                        xss,
                        sqli,
                        sql,
                        csrf,
                        hash,
                        uptime,
                        loadspeed,
                        pagecontent,
                        externallinks,
                        scripts,
                        base64,
                        documenttype,
                        virus,
                        malware,
                        reputation,
                        popups,
                        bruteforce,
                        title,
                        redirect,
                        sensitivedata,
                        emailaddresses,
                        adaissues,
                        accesscontrol,
                        vulnerability,
                        scanned)
                        new_page.save_to_mongo()
                        
                        #return make_response("Thanks", 200)
                        #return render_template('search.html')
        return render_template('/pages/added_page.html')

@page_blueprint.route('/admin/edit_page/<string:page_id>', methods=['POST', 'GET'])
@user_decorators.requires_login #mike added
def edit_page(page_id):
    page = Page.from_mongo_id(page_id)
    if request.method == 'GET':
        
        return render_template('/pages/edit_page.html', page_id=page_id, page= page)
    else:
        domain= request.form['domain']
        user_id= request.form['user_id']
        last_mod= request.form['last_mod']
        timestamp= request.form['timestamp']
        url= request.form['url']
        xss= request.form['xss']
        sqli= request.form['sqli']
        sql= request.form['sql']
        csrf= request.form['csrf']
        hash= request.form['hash']
        uptime= request.form['uptime']
        loadspeed= request.form['loadspeed']
        pagecontent= request.form['pagecontent']
        externallinks= request.form['externallinks']
        scripts= request.form['scripts']
        base64= request.form['base64']
        documenttype= request.form['documents']
        virus= request.form['virus']
        malware= request.form['malware']
        reputation= request.form['reputation']
        popups= request.form['popups']
        bruteforce= request.form['bruteforce']
        title= request.form['title']
        redirect= request.form['redirect']
        sensitivedata= request.form['sensitivedata']
        emailaddresses= request.form['emailaddresses']
        adaissues= request.form['adaissues']
        accesscontrol= request.form['accessontrol']
        vulenrability= request.form['vulnerability']
        scanned= request.form['scanned']
        
        
        edited_page = Page(domain, user_id, last_mod, timestamp,
                           url,
                           xss,
                           sqli,
                           sql,
                           csrf,
                           hash,
                           uptime,
                           loadspeed,
                           pagecontent,
                           externallinks,
                           scripts,
                           base64,
                           documenttype,
                           virus,
                           malware,
                           reputation,
                           popups,
                           bruteforce,
                           title,
                           redirect,
                           sensitivedata,
                           emailaddresses,
                           adaissues,
                           accesscontrol,
                           vulenrability,
                           scanned, page_id)
                           edited_page.update_to_mongo()
                           
        return render_template('/pages/updated_page.html')

@page_blueprint.route('/admin/remove_page/<string:page_id>', methods=['GET'])
@user_decorators.requires_login #mike added
def remove_page(page_id):
    page = page.remove_from_mongo_id(page_id)
    #if request.method == 'GET':
    
    return render_template('/pages/deleted_page.html')
#else:
#title = request.form['title']
#content = request.form['content']
#user = User.get_by_email(session['email'])

#new_post = Post(blog_id, title, content, user.email)
#new_post.save_to_mongo()

#return make_response(blog_posts(blog_id))

@page_blueprint.route('/page_details/<string:page_id>', methods=['GET'])
def show_page(page_id):
    page = page.from_mongo_id(page_id)
    #if request.method == 'GET':
    
    return render_template('/pages/details.html', page_id=page_id, page= page)
#else:
#    title = request.form['title']
#    content = request.form['content']
#    user = User.get_by_email(session['email'])

#    new_post = Post(blog_id, title, content, user.email)
#    new_post.save_to_mongo()

#    return make_response(blog_posts(blog_id))'''


#@user_blueprint.route('/alerts')
#@user_decorators.requires_login
#def user_alerts():
#    user = User.find_by_email(session['email'])
#    return render_template("users/alerts.jinja2", alerts=user.get_alerts())


#@user_blueprint.route('/logout')
#def logout_user():
#    session['email'] = None
#    return redirect(url_for('home'))


#@user_blueprint.route('/check_alerts/<string:user_id>')
#@user_decorators.requires_login
#def check_user_alerts(user_id):
#    pass
