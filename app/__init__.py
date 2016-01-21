# -*- coding: utf-8 -*-
import os
from flask import Flask #class Flask
from flask.ext.sqlalchemy import SQLAlchemy #class SQLAlchemy
from flask.ext.login import LoginManager #class LoginManager
from flask.ext.openid import OpenID #class OpenID
from config import basedir #from module import basedir obj

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app) #create database object
lm = LoginManager()
lm.init_app(app) #configure an application
lm.login_view = 'login' #Flask-Login需要知道哪个函数允许用户登录。
oid = OpenID(app, os.path.join(basedir, 'tmp')) #Flask-OpenID扩展需要一个存储文件的临时文件夹路径
from app import views, models #from folder import modules