from app import db

class CardSets(db.Model):
    __tablename__ = "card_sets"

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), primary_key=True)

    card = db.relationship("Card", backref="sets")
    set = db.relationship("Set", backref="cards")

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    race = db.Column(db.String(255))
    level = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    card_id = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(5000), nullable=False)
    attribute = db.Column(db.String(255))
    link_rating = db.Column(db.Integer)
    rank = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'level': self.level,
            'attack': self.attack,
            'defense': self.defense,
            'card_id': self.card_id,
            'img_url': self.img_url,
            'race': self.race,
            'attribute': self.attribute,
            'link_rating': self.link_rating,
            'rank': self.rank
        }

class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    rarity = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'rarity': self.rarity
        }


