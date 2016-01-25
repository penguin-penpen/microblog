# -*- coding: utf-8 -*-
from flask import flash, render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm, RegisterForm
from app import app, db, lm
from .models import User
from datetime import datetime

@lm.user_loader
def load_user(id):
    return User.query.get(int(id)) #id是unicode字符串??

@app.before_request #register a function to run before every request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    if g.user is None:
        return render_template('index.html',title = 'Home', posts = posts)
    else:
        user = g.user
        posts = ['test1','test2']

        return render_template('index.html',
                               title = 'Home',
                               user = user,
                               posts = posts) #对给定模板传递参数，并翻译模板

@app.route('/register',methods= ['GET','POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(id = 2,
                    nickname = form.nickname.data,
                    password = form.password.data,
                    email = form.email.data,
                    link = form.link.data,
                    about_me = form.about_me.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('register.html',
                           title = 'Register',
                           form = form)

@app.route('/login', methods= ['GET', 'POST'])
def login():
    #创建表单
    form = LoginForm()

    #提交表单的动作
    if form.validate_on_submit():
        if form.password.data == User.query.filter_by(nickname = form.nickname.data).first().getPassword():
            user = User.query.filter_by(nickname = form.nickname.data).first()
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
        session['remember_me'] = form.remember_me.data
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           )

'''
@oid.after_login
#登录完后执行
def after_login(resp): #resp参数包含了从OpenID提供商返回来的信息，email类
    #邮箱为空时，显示错误，重定向到登录页面
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
            #向数据库中添加新用户
            db.session.add(user)
            db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me) #login a user
    #在next页面没有提供的情况下，重定向到首页，否则重定向到next页
    return redirect(request.args.get('next') or url_for('index'))
'''
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User' + nickname + 'not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1'},
        { 'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user = user,
                           posts = posts)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form = form)