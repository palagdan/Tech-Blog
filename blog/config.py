import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SECRET_KEY = '1a2e7da3f62feeb27d0eddd8'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False