#!/usr/bin/python3
from flask import Flask, Blueprint, render_template, request, url_for, redirect, abort
from jinja2 import TemplateNotFound

app.register_blueprint(blueprint)

@app.route('/post')
def post():
    return render_template("post.html")


@app.route('/dashboard')
def dashboard():
    return render_template("admin/index.html")


@app.route('/registered')
def registered():
    return render_template("admin/registered.html")


@app.route('/publishedposts')
def published():
    return render_template("admin/published.html")


@app.route('/manage_post')
def manage_posts():
    return render_template("admin/manage_posts.html")