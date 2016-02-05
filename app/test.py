# -*- coding: utf-8 -*-
from flask import flash, render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import db
from models import Post
import markdown

for i in range(1,8):
    post = db.session.query(Post).filter(Post.id == i).first()
    html_txt = markdown.markdown(post.body_markdown)
    post.body = html_txt
    db.session.add(post)
    db.session.commit()