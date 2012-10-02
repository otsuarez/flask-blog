FlaskBlog
=========


FlaskBlog is another simple blog application, it started being a game to see what Python Framework was lighter. Improvements arrives day by day so feel free to comment whatever you want.


INSTALL
-------

To install FlaskBlog the only dependence you have to resolve is Flask,
Flask-SQLAlchemy and Flask-WTF. We recommend you to create a virtualenv
and run FlaskBlog into. To create a virtualenv you must follow this steps:


	$ sudo easy_install pip
	$ pip install virtualenv
	$ mkdir -p flaskblog/{src,env}
	$ cd flaskblog/
	$ virtualenv --distribute --no-site-packages env/
	$ pip -E env/ install flask
	$ pip -E env/ install flask-wtf
	$ pip -E env/ install flask-sqlalchemy
	$ pip -E env/ install flask-script

Once you've been created the virtualenv you have to clone the
repository on the src/ directory:

	$ hg clone https://bitbucket.org/r0sk/flaskblog src

And that's all, the FlaskBlog was successfully installed on your
computer. Now let's go run it!

RUN
---

To run this amazing piece of software you should enter into virtualenv
mode and then go to src/ directory. First time you run FlaskBlog you
have to initialite the database and insert the user who will manager
the application. Howto do?, running theese commands:

	$ source env/bin/activate
	(env)$ cd src/
	(env)$ python manage.py initdb
	(env)$ python manage.py create_user -u admin -p password
	(env)$ python manage.py runserver
            * Running on http://127.0.0.1:5000/
            * Restarting with reloader

Note, if you run the command create_user as I did, the username is
"admin" and the password is "password" to enter the "admin mode".

Other note, if tou run the command create_user without parameters the
default values are "admin" and "password".

If you want to drop that database and create yours, you can do this
with the dropdb option, the sequence is the following:

    (env)$ cd src/
	(env)$ python manage.py dropdb
	(env)$ python manage.py initdb
	(env)$ python manage.py create_user -u admin -p password
	(env)$ python manage.py runserver
            * Running on http://127.0.0.1:5000/
            * Restarting with reloader

If you open the url (http://127.0.0.1:5000/) in a browser you can see
the index of FlaskBlog. You can configure some parameters of your blog
editing the configuration file, config.py.

Enjot it!.
