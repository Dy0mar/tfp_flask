from flask_mail import Message

from app import db, mail


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    token = db.Column(db.String(255))
    hit = db.Column(db.Integer, default=0)
    access = db.Column(db.Boolean(), default=False)
    email_confirmed = db.Column(db.Boolean(), default=False)

    def send_email_for_confirmation(self, base_url):
        link = f"{base_url}/confirm/{self.token}"
        html = f'Follow the <a href="{link}">link</a> to confirm this email.'
        msg = Message('Hello', recipients=[self.email])
        msg.html = html
        # mail.send(msg)
        print(link)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'token': f'...{self.token[-20:]}',
            'hit': self.hit,
            'access': self.access,
            'email_confirmed': self.email_confirmed,
        }

    def __init__(self, **kwargs):
        for x in kwargs:
            if hasattr(self, x):
                setattr(self, x, kwargs[x])

    def __repr__(self):
        return '<User {}>'.format(self.username)
