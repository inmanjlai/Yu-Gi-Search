from app import db

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    card = db.relationship("Card", backref="comments")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'card_id': self.card_id,
            'content': self.content,
            'user': self.user.to_dict(),
            'card': self.card.to_dict()
        }