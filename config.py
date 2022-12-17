from datetime import timedelta
import os

basedir = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webapp.db')
SECRET_KEY = 'EsvverrGRvev334!svrdev'
REMEMBER_COOKIE_DURATION = timedelta(days=30)
