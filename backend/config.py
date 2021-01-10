import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
databasedir = os.path.join(basedir,'database')
dotenv_path = os.path.join(basedir,'.env')
load_dotenv(dotenv_path)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(databasedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # BOOTSTRAP_BOOTSWATCH_THEME = 'materia'