import os
from datetime import datetime
from flask import Flask, flash, Blueprint, g, render_template, request, abort, session, url_for, redirect
from jinja2 import TemplateNotFound
from models.base_model import User, connect_db, PostTopic, Post, Topic, Contact, Opportunity
from routes.post import post_pages
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from models.model_functions import get_post, manage_author_posts, switcher_role, \
    unapprove, approve, delete_post, signup_register, role, find_author, signin, \
        get_userid, manage_all_posts, posts_available, all_users, delete_user, \
            post_article, addTopic, all_topics, deleteTopic, allowed_member, allowing_a_member, \
                post_opportunity, post_contact
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models.MyForms import LoginForm, RegisterForm, PostForm, ContactForm, OppForm
from flask_simple_captcha import CAPTCHA

from flask import Flask, Blueprint, render_template, request, current_app, url_for, redirect, Markup
from models.model_functions import post_by_slug, find_author, views, all_topics

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, \
    SelectField, FileField, DateTimeField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

import sqlalchemy
from models.base_model import User, Post, Topic, connect_db, Opportunity, Contact
from flask import g, Flask, current_app
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, DateTime, Column, Integer, String, Enum, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
import enum