from flask import Flask, redirect, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import os

# CONFIG ->
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy()
db.init_app(app)
Migrate(app, db)

from models.Card import Card, Set, CardSets

# UTILITY FUNCTIONS TO REUSE IN API ENDPOINTS ->
def request_card(card_name):
    card = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={card_name}")
    return card
def create_sets(card):
    sets = card["card_sets"]
    card_name = card["name"]
    card_to_associate = Card.query.filter(Card.name == card_name).first()

    for set in sets:

        set_in_db = Set.query.filter(Set.name == set["set_name"]).first()

        if not set_in_db:
            new_set = Set(
                name=set["set_name"],
                code=set["set_code"],
                rarity=set["set_rarity"] 
            )
            db.session.add(new_set)
            db.session.commit()

            set_in_db = Set.query.filter(Set.name == set["set_name"]).first()

        
        association_already_exists = CardSets.query.filter(CardSets.card_id == card_to_associate.id, CardSets.set_id == set_in_db.id).first()

        if association_already_exists:
            return "Association already exists between card and set"
        new_association = CardSets(
            card_id=card_to_associate.id,
            set_id=set_in_db.id
        )
        db.session.add(new_association)
        db.session.commit()
def create_card_in_db(card):

    attack = None
    defense = None
    level = None
    attribute = None
    race = None
    link_rating = None
    rank = None

    if "Monster" in card["type"]:
        attack = card['atk']
        attribute = card['attribute']
        race = card['race']

    if "Link" not in card['type'] and "Monster" in card["type"]:
        level = card['level']
        defense = card['def']

    if "Link" in card["type"]:
        link_rating = card['linkval']

    if "XYZ" in card['type']:
        rank = card["level"]
    
    add_to_db = Card(
        name=card["name"],
        description=card["desc"],
        type=card["type"],
        race=card["race"],
        card_id=card["id"],
        img_url=card["card_images"][0]["image_url"],
        attack=attack,
        defense=defense,
        level=level,
        attribute=attribute,
        link_rating=link_rating,
        rank=rank
    )

    db.session.add(add_to_db)
    db.session.commit()

    create_sets(card)

# FIGURE OUT HOW TO MAKE get_card_by_name A CASE INSENSITIVE QUERY ->
def get_card_by_name(card_name):
    card = Card.query.filter(Card.name == card_name).first()
    if card:
        return card.to_dict()
    else:
        return {"Error": f"Card '{card_name}' could not be found"}
def get_cards_like_name(card_name):
    cards = Card.query.filter(Card.name.ilike("%" + card_name + "%")).all()
    if cards:
        return [card.to_dict() for card in cards]
    else:
        return {"Error": f"Card '{card_name}' could not be found"}
def get_card_sets(card):
    card_id = card["id"]
    cards_and_sets = CardSets.query.filter(CardSets.card_id == card_id).all()
    set_ids = [set.set_id for set in cards_and_sets]
    sets = []
    for id in set_ids:
        set = Set.query.get(id)
        sets.append(set)

    return [set.to_dict() for set in sets]

def get_cards_paginated(card_name, page_number):
    cards = Card.query.filter(Card.name.ilike('%' + card_name + '%')).paginate(page=page_number, per_page=50)
    return cards

# APP ROUTES ->
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cards/search/page/<int:page_number>", methods=["POST"])
def search_paginated(page_number):
    card_name = request.form.get("card-name")
    print("SEARCHING 50 CARDS WITH", card_name, "PAGE:", page_number)

    paginated_cards = get_cards_paginated(card_name=card_name, page_number=page_number)
            
    if "Error" in paginated_cards:
        fetch_card = request_card(card_name)
        if fetch_card.ok:
            create_card_in_db(fetch_card.json()["data"][0])
            card_fetched = get_card_by_name(fetch_card.json()["data"][0]["name"])
            card_fetched_sets = get_card_sets(card_fetched)
            return render_template("card.html", card=card_fetched, sets=card_fetched_sets)
        else:
            return render_template("home.html", error="No cards found with given name")
    else:
        if len(paginated_cards.items) == 1:
                return render_template("card.html", card=paginated_cards.items[0])
        return render_template(
            "cards.html", 
            cards=paginated_cards.items, 
            card_name=card_name, 
            page_number=paginated_cards.page, 
            prev=paginated_cards.has_prev, 
            next=paginated_cards.has_next
        )

@app.route("/card/<card_name>")
def card(card_name):
    card = get_card_by_name(card_name)

    sets = get_card_sets(card)

    if "Error" not in card:
        return render_template("card.html", card=card, sets=sets)
    else:
        error = f"{card_name} was not found"
        return render_template("home.html", error=error)

# @app.route("/fetch_all_cards")
# def seed():
    all_cards = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")

    for card in all_cards.json()["data"]:
        if "card_sets" in card:
            create_card_in_db(card)

    return "CARDS SEEDED"