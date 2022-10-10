from app import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(1000), nullable=False)
    bio = db.Column(db.String(3000))

    comments = db.relationship("Comment", backref="user", lazy=True)


    def to_dict(self):
        return{
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'username': self.username,
            'hashed_password': self.hashed_password,
            'bio': self.bio,
            'decks': [deck.to_dict() for deck in self.decks]
        }
    
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
