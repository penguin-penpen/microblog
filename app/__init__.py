# -*- coding: utf-8 -*-
import os
from flask import Flask #class Flask
from flask.ext.sqlalchemy import SQLAlchemy #class SQLAlchemy
from flask.ext.login import LoginManager #class LoginManager
from flask.ext.openid import OpenID #class OpenID
from config import basedir #from module import basedir obj

from momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app) #create database object
lm = LoginManager()
lm.init_app(app) #configure an application
lm.login_view = 'login' #Flask-Login需要知道哪个函数允许用户登录。
#oid = OpenID(app, os.path.join(basedir, 'tmp')) #Flask-OpenID扩展需要一个存储文件的临时文件夹路径
app.jinja_env.globals['momentjs'] = momentjs #告诉Jinja2导入momentjs类作为所有模板的全局变量
from app import views, models #from folder import modules   此行不能提前到脚本开头，为什么？