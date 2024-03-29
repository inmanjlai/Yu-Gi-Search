from app import db
import requests

class CardSets(db.Model):
    __tablename__ = "card_sets"

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), primary_key=True)
    set_price = db.Column(db.Float())
    set_rarity = db.Column(db.String(500))

    card = db.relationship("Card", backref="sets", cascade="all,delete")
    set = db.relationship("Set", backref="cards", cascade="all,delete")

    def to_dict(self):

        print(self.set.to_dict(), "HERE")

        return {
            "card_id": self.card_id,
            "set_id": self.set_id,
            "set_price": self.set_price,
            "set_rarity": self.set_rarity,
            "set": self.set.to_dict()
        }

class DeckList(db.Model):
    __tablename__ = "decklists"

    card_id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    # card = db.relationship("Card", backref="decks")
    deck = db.relationship("Deck", back_populates="cards")

    def to_dict(self):
        return {
            'card_id': self.card_id,
            'deck_id': self.deck_id
        }

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
    lowest_price = db.Column(db.Float())

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
            'rank': self.rank,
            'lowest_price': self.lowest_price
        }

class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }

class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cover_img = db.Column(db.String(4000))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    cards = db.relationship("DeckList", cascade="all, delete, delete-orphan", back_populates="deck")
    user = db.relationship("User", backref="decks")

    def get_decklist(self):
        decklist = DeckList.query.filter(DeckList.deck_id == self.id).all()
        main_deck = []
        extra_deck = []
        for card in decklist:
            card_object = Card.query.get(card.card_id).to_dict()
            card_object["quantity"] = card.quantity
            if "XYZ" not in card_object["type"] and "Link" not in card_object["type"] and "Fusion" not in card_object["type"] and "Synchro" not in card_object["type"]:
                main_deck.append(card_object)
            else:
                extra_deck.append(card_object)

        deck = {"main_deck": [card for card in main_deck], "extra_deck": [card for card in extra_deck]}
        return deck

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'cards': self.cards,
            'cover_img': self.cover_img
        }

