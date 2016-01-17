# -*- coding: utf-8 -*-
from flask import flash, render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from app import app, db, lm, oid
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id)) #id是unicode字符串??

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
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
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    #创建表单
    form = LoginForm()

    #提交表单的动作
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    #以GET方式请求页面是返回html
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp): #rep参数包含了从OpenID提供商返回来的信息
    #邮箱为空
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    #从数据库中搜索邮箱地址，如果邮箱地址不在数据库中，为新用户。
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
            user = User(nickname=nickname, email=resp.email)
            db.session.add(user)
            db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    #在next页面没有提供的情况下，重定向到首页，否则重定向到next页
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user