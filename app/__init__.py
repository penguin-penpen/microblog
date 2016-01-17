# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app) #create database object
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' #Flask-Login需要知道哪个函数允许用户登录。
oid = OpenID(app, os.path.join(basedir, 'tmp')) #Flask-OpenID扩展需要一个存储文件的临时文件夹路径
from app import views, models