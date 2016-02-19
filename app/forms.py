__author__ = 'yang'
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email address', [DataRequired(), Email()])
    password = PasswordField('password', [DataRequired()])
    confirm = PasswordField('repeat Password',
                            [DataRequired(),
                            EqualTo('password', message='Passwords must match')])
    link = StringField('link')
    about_me = TextAreaField('about_me', validators=[DataRequired()])
    #recaptcha = RecaptchaField()

class LoginForm(Form):
    nickname = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class CommentForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    comment = TextAreaField('comment', validators=[DataRequired()])