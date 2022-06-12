"""
Application configuration file. Do not hardcode passwords or secret strings here
"""

class Config:
    SECRET_KEY = 'asdmnc5b4734-+*23'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    MAIL_SERVER='smtp.mail.yahoo.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'smaiabba@yahoo.com'
    MAIL_PASSWORD = 'iwyeqezrldpmcycv'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    STAFF_MAIL_PATTERNS = ['kadunapolytechnic.edu.ng', 'kadpoly.gov.ng']
    SALT_PASSWORD = 'asldm7n3c_+w(&3984'
    
    @staticmethod
    def init_app():
        pass