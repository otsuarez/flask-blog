from __future__ import absolute_import
from flask.ext.script import Manager, Option
from blog import app, db

manager = Manager(app)

@manager.command
def initdb():
    """Creates all database tables."""
    db.create_all()

@manager.option('-u','--user', dest='user', default='admin', help='Username')
@manager.option('-p','--password', dest='password', default='password', help='Password')
def create_user(user, password):
    """Creates the admin user."""
    from blog import User
    u=User(user, password)
    db.session.add(u)
    db.session.commit()

@manager.command
def dropdb():
    """Drops all database tables."""
    db.drop_all()

if __name__ == '__main__':
    manager.run()
