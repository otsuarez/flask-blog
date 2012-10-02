# -*- coding: utf-8 -*-
#import pdb;pdb.set_trace()


"""
FlaskBlog
~~~~~~~~~~~~~~
:copyright: (c) 2011 by Oscar M. Lage.
:license: BSD, see LICENSE for more details.
"""

#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash
from werkzeug.routing import Rule
from flaskext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     validators

#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# MIDDLEWARE (to serve static files)
#------------------------------------------------------------------------------#
# Middleware to serve the static files
from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})

#------------------------------------------------------------------------------#
# FUNCTIONS
#------------------------------------------------------------------------------#
from unicodedata import normalize

# Slug (https://gist.github.com/1428479)
def slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return unicode(''.join(strict_text))

#------------------------------------------------------------------------------#
# MODELS
#------------------------------------------------------------------------------#
# Model
class Post(db.Model):
    """Post model - storing posts in db"""
    __tablename__ = 'Posts'
    __mapper_args__ = dict(order_by="date desc")

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Unicode(255))
    slug = db.Column(db.Unicode(255))
    author = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    content = db.Column(db.Text())

    def __init__(self, subject, content):
        self.subject = subject
        self.slug = slug(subject)
        self.content = content
        #self.author = g.user.id
        self.date = datetime.utcnow()

class User(db.Model):
    """User model - storing users in db"""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    passwd = db.Column(db.String(30))

    def __init__(self, name=None, passwd=None):
        self.name = name
        self.passwd = passwd

#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#
# Create Form
class CreateForm(Form):
    """Form used to create a new post"""
    subject = TextField('Subject', [validators.required()])
    content = TextAreaField('Content', [validators.required(), 
                                        validators.Length(min=1)])

# Login form
class LoginForm(Form):
    """Form used to login into the system"""
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])


#------------------------------------------------------------------------------#
# CONTROLLERS
#------------------------------------------------------------------------------#
# Hook before request (check user session)
@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

# Index
@app.route('/')
def index():
        return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    posts = Post.query.order_by(Post.date.desc()).all(),)

# Post detail
@app.route('/<path:slug>.html')
def post(slug):
        return render_template(app.config['DEFAULT_TPL']+'/post.html',
			    conf = app.config,
			    post = Post.query.filter(Post.slug == slug).first_or_404())

# Add a new post
@app.route('/add', methods=['GET','POST'])
def add():
    if g.user is None:
        return redirect(url_for('login'))
    else:
	if request.method == 'POST':
		post = Post(request.form['subject'], request.form['content'])
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template(app.config['DEFAULT_TPL']+'/form.html',
			       conf = app.config,
			       form = CreateForm())

# Edit a post
@app.route('/edit/<path:slug>.html', methods=['GET','POST'])
def edit(slug):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        post = Post.query.filter(Post.slug == slug).first_or_404()
        form = CreateForm(request.form, subject=post.subject, content=post.content)
	if request.method == 'POST' and form.validate():
                post.subject = request.form['subject']
                post.content = request.form['content']
		db.session.commit()
		return redirect(url_for('index'))
	return render_template(app.config['DEFAULT_TPL']+'/form.html',
			       conf = app.config,
			       form = form)

@app.route('/delete/<path:slug>.html')
def delete(slug):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        post = Post.query.filter(Post.slug == slug).first_or_404()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))
    

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Invalid username or password.'
            else:
                print u.id
                session['logged_in'] = True
                session['user_id'] = u.id
                session['user_name'] = u.name
                flash('You were logged in')
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))

# User Logout
@app.route('/logout')
def logout():
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        flash('You were logged out')
    return redirect(url_for('index'))

#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run()
