from blog import db, login_manager, app
from blog import bcrypt
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    image_file = db.Column(db.String(length=20), nullable=False, default='default.jpg')
    password = db.Column(db.String(length=60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode()

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    @property
    def passwordHash(self):
        return self.password

    @passwordHash.setter
    def passwordHash(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'Username: {self.username} Email: {self.email} Password: {self.password}'

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    content = db.Column(db.String(length=5000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'title: {self.title} content: {self.content}'
