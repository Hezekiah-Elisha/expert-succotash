#!/usr/bin/python3
import os
from datetime import datetime
from flask import Flask, flash, Blueprint, g, render_template, request, abort, session, url_for, redirect
from jinja2 import TemplateNotFound
from models.base_model import User, connect_db, PostTopic, Post, Topic
from routes.post import post_pages
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from models.model_functions import get_post, manage_author_posts, switcher_role, \
    unapprove, approve, delete_post, signup_register, role, find_author, signin, \
        get_userid, manage_all_posts, posts_available, all_users, delete_user, \
            post_article, addTopic, all_topics, deleteTopic, allowed_member, allowing_a_member
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models.MyForms import LoginForm, RegisterForm, PostForm
from flask_simple_captcha import CAPTCHA


app = Flask(__name__)
app.secret_key = '68dfac8f4ac79a8532745e899de14428'
app.register_blueprint(post_pages)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    f"mysql+mysqldb://{'root'}:{'root'}@localhost/{'this_blog'}"

db = SQLAlchemy(app)

app.engine = connect_db()
db.create_all()
now = datetime.now()

CAPTCHA_CONFIG = {'SECRET_CAPTCHA_KEY':'6fd916492b7931ca22034a3959a01f9e'}
CAPTCHA = CAPTCHA(config=CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# g.session_db = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_first_request
def create_db():
    Session = sessionmaker(bind=app.engine)
    User.__table__.create(bind=app.engine, checkfirst=True)
    Post.__table__.create(bind=app.engine, checkfirst=True)
    Topic.__table__.create(bind=app.engine, checkfirst=True)
    PostTopic.__table__.create(bind=app.engine, checkfirst=True)
    # g.session_db = None
    
    # g.session_db = Session()
    # db.create_all()
    


@app.errorhandler(404)
def error(error):
    name = "page"
    return render_template('404.html', name=name), 404 


@app.route('/', defaults={'page': 'home'})
@app.route('/<page>')
def html_lookup(page):
    try:
        m = all_topics()
        posts = posts_available()
        return render_template('{}.html'.format(page), message="Welcome to this space", posts=posts, year=now.year, m=m)
    except TemplateNotFound:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session.pop('username', None)
        
        if request.method == 'POST':
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if CAPTCHA.verify(c_text, c_hash):
                if form.validate_on_submit():
                    areyouuser = form.username.data
                
                    pwd = signin(areyouuser)
                    if pwd is not None:
                        if check_password_hash(pwd, form.password.data):
                            session['username'] = areyouuser
                            session['role'] = role(areyouuser)
                            session['id'] = get_userid(areyouuser)
                            session['allowed'] = allowed_member(areyouuser)
                            return redirect(url_for('html_lookup'))
                        else:
                            flash("Please enter the correct password or username")
                            return render_template('error.html', form=form, captcha=CAPTCHA.create())
                            # raise
                    else:
                        flash('Please enter the correct password or username')
                        return render_template('error.html', form=form, captcha=CAPTCHA.create())
            else:
                flash('Failed captcha, please log in again!')
                return render_template('error.html', form=form, captcha=CAPTCHA.create())
    captcha = CAPTCHA.create()
    return render_template('login.html', form=form, captcha=captcha)

@app.route('/getsession')
def getsession():
    if 'username' and 'role' and 'id' in session:
        return f"{g.username} : {g.role} : {g.id}: {g.allowed}"
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.username = None
    g.role = None
    g.id = None
    g.allowed = ""
    if 'username' in session:
        g.username = session['username']
        g.role = session['role']
        g.id = session['id']
        g.allowed = session['allowed']   


@app.route('/register', methods=['POST','GET'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.firstName.data
        last_name = form.lastName.data
        email = form.email.data
        gender = form.gender.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data

        if password==password_confirmation:
            password_confirmed = password
            message = signup_register(username.lower(), first_name.title(), last_name.title(), gender, email, generate_password_hash(password_confirmed))
            return render_template('register.html', message=message, form=form)
        else:
            message = "Password and password confirmation do not match"
            return render_template('register.html', form=form, message=message)
    message = 'Please sign up'
    return render_template('register.html', message=message, form=form)


@app.route('/posts')
def posts():
    m = all_topics()
    posts = posts_available()
    return render_template('posts.html', m=m, posts=posts)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('html_lookup'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        print(g.username, g.allowed)
        return render_template('admin/index.html', user=g.username)
    else:
        return redirect(url_for('login'))


@app.route('/registered', methods=['POST', 'GET'])
def registered_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        users = all_users()
        return render_template('admin/registered.html', users=users)
    # else:
    #     # role = request.form['role']
    #     # name = find_author(id)
    #     # change_it = switcher_role(name, role)
    #     return redirect(url_for('admin/registered_list'))


@app.route('/add-topic', methods=['POST', 'GET'])
def add_topic():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        all = all_topics()
        return render_template('admin/add_topic.html', all=all)
    else:
        topic_name = request.form['topic_name']
        slug = topic_name.lower().replace(' ', '-')
        message = addTopic(topic_name, slug)
        # return render_template('admin/add_topic.html', message=message)
        return redirect(url_for('dashboard'))
    
app.route('/change_role/<username>_<role>')
def change_role(username, role):
    # if 'username' not in session:
        # return redirect(url_for('login'))
        # role = request.form['role']
    # switch = switcher_role(username, role)
    return redirect(url_for('registered_list'))


@app.route('/allow-<username>')
def allow_a_member(username):
    changed = allowing_a_member(username)
    return 'weweweweweewewe'



@app.route('/delete/<id>')
def deleted_user(id):
    delete = delete_user(id)
    return redirect(url_for('registered_list'))

@app.route('/delete_topic/<id>')
def delete_topic(id):
    deleteTopic(id)
    return redirect(url_for('add_topic'))


@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'GET':
        if 'username' in session:
            m = all_topics()
            return render_template("admin/create_post.html", message="This is a get method", user=g.username, m=m)
        else:
            return redirect(url_for('login'))
    else:

        if 'username' in session:
            title = request.form['title']
            body = request.form['body']
            topic = request.form['topic']
            banner = request.files['file']
            credit = request.form['credit']

        if banner.filename == '':
            return redirect(request.url)
        if banner and allowed_file(banner.filename):
            filename = secure_filename(banner.filename)
            banner.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # banner.save(f'/static/images/{filename}')
            # return redirect(url_for('uploaded_file', filename=filename))

            user_id = get_userid(g.username)
            message = post_article(title, filename, body, topic, user_id, credit)
            return render_template('admin/index.html', message=message)
        else:
            return redirect(url_for('login'))
    
@app.route('/manage_posts')
def manage_posts():
    if 'username' in session:
        if g.role == 'super_user' or g.role == 'Admin':
            posts = manage_all_posts()
            return render_template("admin/manage_posts.html", posts=posts, user=g.username)
        else:
            posts = manage_author_posts(g.username)
            return render_template('admin/manage_posts.html', posts=posts, user=g.username)
    else:
        return redirect(url_for('login'))

@app.route('/approve/<id>')
def approved_post(id):
    approving = approve(id)
    return redirect(url_for('manage_posts'))


@app.route('/unapprove/<id>')
def unapproved_post(id):
    unapproving = unapprove(id)
    return redirect(url_for('manage_posts'))

@app.route('/delete_post/<id>')
def deleted_post(id):
    delete = delete_post(id)
    return redirect(url_for('manage_posts'))


@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def editting(id):
    if 'username' in session:
        if request.method == 'GET':
            post = get_post(id)
            post.title = request.form['title']
            return render_template('admin/edit_post.html')#, post=post)
        else:
            pass
    else:
        return redirect(url_for('login'))


@app.route('/published')
def published():
    posts = manage_all_posts()
    return render_template('admin/published.html', posts=posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
