import os
DEBUG = True

_basedir = os.path.abspath(os.path.dirname(__file__))

DATA_PATH = os.path.join(_basedir, 'data')
DEFAULT_TPL = 'default'

SECRET_KEY = 'secret devel key'

URL = 'http://localhost:8080/'
TITLE = 'FlaskBlog'
VERSION = '0.1.3'
LANG = 'es'
LANG_DIRECTION = 'ltr'
YEAR = '2012'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(os.path.dirname(__file__), 'database.db')
SQLALCHEMY_DATABASE_URI = 'mysql://flaskuser:asecretpass@localhost/myflask'

del os
