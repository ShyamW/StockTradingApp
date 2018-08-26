import os
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = '7d441f27d441f27567d441f2b6176a'

# Flask-User settings
USER_APP_NAME = "Stock App"
USER_ENABLE_EMAIL = False  # No email authentication
USER_ENABLE_USERNAME = True  # Just use username auth
USER_REQUIRE_RETYPE_PASSWORD = True  # Make user retype password
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
DEBUG = True
