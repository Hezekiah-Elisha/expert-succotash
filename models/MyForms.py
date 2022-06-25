#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, \
    SelectField, FileField, DateTimeField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    firstName = StringField('FirstName', validators=[DataRequired()])
    lastName = StringField('LastName', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    gender = SelectField(u'gender', choices=[('male', 'man'), ('female', 'woman'), ('prefer not to say', 'None')])
    password = PasswordField('password', validators=[DataRequired()])
    password_confirmation = PasswordField('password1', validators=[DataRequired()])
    submit = SubmitField('submit')


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    banner = FileField('banner', validators=[FileRequired()])
    body = StringField('body', validators=[DataRequired()])
    credit = StringField('credit', validators=[DataRequired()])
    topic = SelectField(u'topic', coerce=int, validators=[DataRequired()])
    submit = SubmitField('submit')


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    feedback = TextAreaField('feedback', validators=[DataRequired()])
    submit = SubmitField('submit')

class OppForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    topic = StringField('topic', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    link = StringField('link', validators=[DataRequired()])
    expiry_date = DateTimeField('date', validators=[DataRequired()])
    submit = SubmitField('submit')
