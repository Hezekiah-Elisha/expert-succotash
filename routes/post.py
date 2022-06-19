from flask import Flask, Blueprint, render_template, request, current_app, url_for, redirect, Markup
from models.model_functions import post_by_slug, find_author, views

post_pages = Blueprint("posts", __name__)

@post_pages.get("/post/<slugg>")
def display_post(slugg):
    slugg = slugg.replace(' ', '_')
    post_details = post_by_slug(slugg)
    name = "Post"
    if post_details:
        name = find_author(post_details.user_id)
   
        # Markup(post_details.body).striptags()
        post_a_views=views(post_details.views)

    
        return render_template("post.html", title=post_details.title, slug=post_details.slug, first_name=name.first_name, last_name=name.last_name, banner=post_details.banner,\
            body=post_details.body, views=post_a_views, dop=post_details.dop)
    return render_template("404.html", name=name)

