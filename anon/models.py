from itsdangerous.url_safe import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, login_manager
from flask_login import UserMixin
from flask import current_app
from flask import current_app



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    f_name = db.Column(db.String(128))
    m_name = db.Column(db.String(128))
    l_name = db.Column(db.String(128))
    gender = db.Column(db.CHAR(1))
    address = db.Column(db.String(128))
    phone = db.Column(db.CHAR(11))
    state = db.Column(db.String(64))

    # next of kin information
    nk_full_name = db.Column(db.String(128))
    nk_address = db.Column(db.String(128))
    nk_relation = db.Column(db.String(128))


    # car information
    plate_number = db.Column(db.String(16), unique=True, index=True)
    model = db.Column(db.String(64))
    color = db.Column(db.String(64))

    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        """Returns a printable format of the user object"""
        return '<{} - {} {}, {}>'.format(self.id, self.f_name, self.l_name, self.plate_number)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.id, salt=current_app.config['SALT_PASSWORD'])

    def confirm_token(self, token):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(
                token,
                salt = current_app.config['SALT_PASSWORD'],
                max_age=1800
            )
        except:
            return False
        if data != self.id:
            return False
        # confirm and activate user
        self.is_confirmed = True
        self.is_active = True
        db.session.add(self)
        return True


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    is_super = db.Column(db.Boolean())
    is_active = db.Column(db.Boolean(), default=True)

    @property
    def password(self):
        raise AttributeError('PROPERTY NOT ACCESSIBLE.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Returns a printable format of the user object"""
        return '<Admin {} - {}>'.format(self.id, self.user_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)