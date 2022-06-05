from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, DateTime, Column, Integer, String, Enum, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
import enum

Base = declarative_base()

# class MyEnum(enum.Enum):
#     super_user = 1
#     admin = 2
#     author = 3 



class User(Base):
    """
    Class User; instance of Base
    """
    __tablename__ = "users"
    user_id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    gender = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    reg_datetime = datetime.now()
    password = Column(String(255), nullable=False)
    # role = Column('role', Enum(MyEnum))
    role = Column(String(10), unique=False, nullable=False)

    posts = relationship("Post", cascade="all, delete-orphan")#, backref="users")



class Post(Base):
    """
    Post table
    """
    __tablename__= "posts"
    post_id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), nullable=False)
    banner = Column(String(250), nullable=False)
    body = Column(LONGTEXT, nullable=False)
    topic = Column(String(200), nullable=False)
    views = Column(Integer, unique=False, nullable=False)
    approved = Column(Boolean, nullable=False)
    dop = Column(DateTime, default=datetime.now, nullable=False)
    dom = Column(DateTime, default=datetime.now, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    users = relationship("User", back_populates="posts")
    post_topics = relationship("PostTopic", cascade="all, delete-orphan", backref="posts_pt")
    topics_pt = relationship("Post", cascade="all, delete-orphan", backref="PostTopics")


class Topic(Base):
    """
    Topic Base
    """
    __tablename__="topics"
    topic_id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String(40), nullable=False)
    slug = Column(String(255), nullable=False)

    PostTopics = relationship("PostTopic", cascade="all, delete-orphan", backref="topics_pt")
    posts_pt = relationship("Topic", cascade="all, delete-orphan", backref="post_topics")


class PostTopic(Base):
    """
    table PostTopic
    """
    __tablename__="post_topic"
    post_topic_id = Column(Integer, nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), unique=True)
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), unique=True)


def connect_db():
    db = create_engine(f"mysql+mysqldb://{'root'}:{'root'}@localhost/{'this_blog'}", pool_pre_ping=True, echo=True)
    return db

# engine = connect_db()
# User.__table__.create(bind=engine, checkfirst=True)
# Post.__table__.create(bind=engine, checkfirst=True)
# Topic.__table__.create(bind=engine, checkfirst=True)
# PostTopic.__table__.create(bind=engine, checkfirst=True)