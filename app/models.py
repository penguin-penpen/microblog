# -*- coding: utf-8 -*-
from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index = True, unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(120), index=True, unique=True)
    link = db.Column(db.String(100)) #个人链接
    messages = db.relationship('Message', backref='author', lazy='dynamic') #留言
    about_me = db.Column(db.String(140))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)    #python2
        except NameError:
            return str(self.id)    #python3

    def __repr__(self): #define how to print db info
        return '<User %r>' % (self.nickname)

    def getPassword(self):
        return self.password

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #初始化为外键，因此这个字段是连接到用户上

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # body显示储存html格式
    body = db.Column(db.String)
    timestamp = db.Column(db.String)
    info = db.Column(db.String)
    body_markdown = db.Column(db.String)
    counter = db.Column(db.Integer)
    lan_used = db.Column(db.String)

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String)

class PostTagRel(db.Model):
    tag_rel_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.tag_id))
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))