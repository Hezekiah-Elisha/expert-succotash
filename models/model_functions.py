#!/usr/bin/python3
import sqlalchemy
from models.base_model import User, Post, Topic, connect_db
from flask import g, Flask, current_app
from sqlalchemy.orm import sessionmaker

# app = Flask(__name__)
engine = connect_db()

Session = sessionmaker(bind=engine)
session = Session()


def signup_register(username, first_name, last_name, gender, email, password, role='Author'):
    try:
        user = User(username=username, first_name=first_name, last_name=last_name, gender=gender,\
            email=email, password=password, role=role)
        # print(session)
        session.add(user)
        session.commit()
        return('Kindly proceeed to the log in page. Thank You!')
    except:
        session.rollback()
        raise


def signin(username):
    # user = User.query.filter_by(username=usernamet).first()
    try:
        user = session.query(User).filter(User.username==username).first()
        if user is not None:
            return(user.password)
        else:
            return None
    except:
        raise

def posts_available():
    posts = session.query(Post).limit(10)
    return posts


def manage_all_posts():
    posts = session.query(Post).all()
    return posts


def post_by_slug(slug):
    by_slug = session.query(Post).filter(Post.slug==slug).first()
    return by_slug


def find_author(id):
    name = session.query(User).filter(User.user_id==id).first()
    return name


def get_userid(username):
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        return(user.user_id)
    else:
        return None


def manage_author_posts(username):
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        posts = session.query(Post).filter(Post.user_id==user.user_id).all()
        return posts
    else:
        return None


def all_users():
    users = session.query(User)
    return users


def switcher_role(username, role):
    try:
        user_roles = session.query(User).filter(User.username==username).first()
        user_roles.role = role
        session.commit()
        return "Updated to different"
    except:
        session.rollback()
        raise


def delete_user(id):
    user_gone = session.query(User).get(id)
    session.delete(user_gone)
    session.commit()
    return "Deleted"


def post_article(title, banner, body, topic, user_id, approved=0,  views=0):
    try:
        slug = title.replace(' ', '_')
        post = Post(title=title, slug=slug, banner=banner, body=body, topic=topic, user_id=user_id, approved=approved, views=views)
        session.add(post)
        session.commit()
        return "Posted succefully"
    except:
        session.rollback()
        raise


def get_post(id):
    post = session.query(Post).filter(Post.user_id==id).first()
    if post is not None:
        return post
    return None


def views(post_views):
    try:
        post_a = session.query(Post).filter(Post.views == post_views).first()
        post_a.views += 1
        session.commit()
        return post_a.views
    except:
        session.rollback()
        raise

def role(username):
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        return(user.role)
    else:
        return None

def approve(id):
    try:
        post_update = session.query(Post).filter(Post.post_id==id).first()
        post_update.approved = True
        session.commit()
        return "Updated"
    except:
        session.rollback()
        raise


def unapprove(id):
    try:
        post_update = session.query(Post).filter(Post.post_id==id).first()
        post_update.approved = False
        session.commit()
        return "Updated to false"
    except:
        session.rollback()
        raise


def delete_post(id):
    delete_post_here = session.query(Post).get(id)
    session.delete(delete_post_here)
    session.commit()
    return "Deleted"

def addTopic(topic, slug):
    try:
        topic_add = session.query(Topic).filter(Topic.name==topic).first()
        if topic_add is None:
            topic_add = Topic(name=topic, slug=slug)
            session.add(topic_add)
            session.commit()
            return "Added"
        else:
            return "Already exists"
    except:
        session.rollback()
        raise


def all_topics():
    try:
        all_topics = session.query(Topic)
        return all_topics
    except:
        raise
