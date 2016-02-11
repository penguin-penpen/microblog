# -*- coding: utf-8 -*-
from flask import flash, render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, EditForm, RegisterForm
from app import app, db, lm
from .models import User, Post, Tag, PostTagRel, Series
from datetime import datetime
import markdown
import markdown2

# 初始化首页加载次数
index_add_counter = 0
# 获取文章分类
series = db.session.query(Series.series_name).order_by(Series.series_id).all()
# classification = [r(0).encode('utf8') for r in classification]
# for tag in db.session.query(Tag.tag_name).order_by(Tag.tag_id).all():
#     global classification
#     classification.append(str(tag))

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

"""
tags为字典，{post_id : tag_id}
倒序输出post
"""
@app.route('/')
@app.route('/index')
def index():
    # 声明全局变量
    global  index_add_counter
    global series
    index_add_counter = 0
    posts = []
    tags = {}
    # 根据加载次数计算相对post_id，一次加载10篇
    for post_id in range(10 * index_add_counter + 1, 10 * index_add_counter + 11):
        tags.setdefault(post_id, [])
        try:
            post = db.session.query(Post).order_by(db.desc(Post.id))[post_id - 1]
            posts.append(post)

            for tag_id in (db.session.query(PostTagRel).filter(PostTagRel.id == post_id).first().tag_id.split(',')):
                tag = db.session.query(Tag).filter(Tag.tag_id == tag_id).first().tag_name
                tags[post_id].append(tag)
        except IndexError:
            # posts.reverse()
            index_add_counter += 1
            return render_template('index.html',
                                   title = 'Home',
                                   series = series,
                                   user = user,
                                   posts = posts,
                                   tags = tags)
    # posts.reverse()
    index_add_counter += 1
    return render_template('index.html',
                           title = 'Home',
                           series = series,
                           user = user,
                           posts = posts,
                           tags = tags) #对给定模板传递参数，并翻译模板

@app.route('/index-addition')
def index_addition():
    # 声明全局变量
    global index_add_counter
    posts = []
    tags = {}
    # 根据加载次数计算相对post_id
    for post_id in range(10 * index_add_counter + 1, 10 * index_add_counter + 11):
        tags.setdefault(post_id, [])
        try:
            post = db.session.query(Post).order_by(db.desc(Post.id))[post_id - 1]
            posts.append(post)

            for tag_id in (db.session.query(PostTagRel).filter(PostTagRel.id == post_id).first().tag_id.split(',')):
                tag = db.session.query(Tag).filter(Tag.tag_id == tag_id).first().tag_name
                tags[post_id].append(tag)
        except IndexError:
            # posts.reverse()
            index_add_counter += 1
            return render_template('index-addition.html',
                                   title = 'Home',
                                   user = user,
                                   posts = posts,
                                   tags = tags)
    # posts.reverse()
    index_add_counter += 1
    return render_template('index-addition.html',
                           title = 'Home',
                           user = user,
                           posts = posts,
                           tags = tags) #对给定模板传递参数，并翻译模板

"""
用文章id从数据库查询相应内容并显示
"""
@app.route('/post/<post_id>')
def post(post_id):
    post = db.session.query(Post).filter(Post.id == post_id).first()
    html_txt = markdown.markdown(post.body_markdown, extensions=['fenced_code'])
    post.body = html_txt
    db.session.add(post)
    db.session.commit()
    tags = []
    # tag = db.session.query(Tag).join(PostTagRel).filter(PostTagRel.id == post_id).first().tag_name
    for tag_id in (db.session.query(PostTagRel).filter(PostTagRel.id == post_id).first().tag_id.split(',')):
                tag = db.session.query(Tag).filter(Tag.tag_id == tag_id).first().tag_name
                tags.append(tag)
    return render_template('post.html',
                           title = Post.title,
                           series = series,
                           post = post,
                           tags = tags)

# 归档页面
# 用js实现不加载按时间排序或按类别排序
# archives页面根据post_id倒序排列，默认以时间为序
@app.route('/archives')
def archives():
    posts = db.session.query(Post).order_by(db.desc(Post.id)).all()
    return render_template('archives.html',
                           title = 'Archives',
                           series = series,
                           posts = posts)

@app.route('/archives/<tag>')
def archives_tag(tag):
    return render_template('archives.html',
                           title = str(tag),
                           post = post)

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

# 测试页面
@app.route('/testBootstrap')
def test():
    return render_template('testBootstrap.html')

@app.route('/addition')
def addition():
    return render_template('addition.html')

