# -*- coding: utf-8 -*-
__author__ = 'yang'
from app import app
from flask import render_template
from flask import flash
from flask import redirect
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': {'Beautiful day in portland'}
        },
        {
            'author': {'nickname': 'Susan'},
            'body': {'The Avengers movie was so cool!'}
        }
    ]

    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           posts = posts)

@app.route('/login', methods= ['GET', 'POST'])
def login():
    #创建表单
    form = LoginForm()

    #提交表单的动作
    if form.validate_on_submit():

        #显示信息
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        #处理完后重定向到首页
        return redirect('/index')
    #以GET方式请求页面是返回html
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])
