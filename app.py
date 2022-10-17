from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, render_template, request, json, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user
from sqlalchemy import func
import requests
import os

# CONFIG ->
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db = SQLAlchemy()

login_manager = LoginManager(app)

db.init_app(app)
Migrate(app, db)

from models.Card import Card, Set, CardSets, Deck, DeckList
from models.User import User
from models.Comment import Comment
from flask.cli import AppGroup

seed_commands = AppGroup('seed')

def seed_cards():
    all_cards = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")

    for card in all_cards.json()["data"]:
        if "card_sets" in card:
            create_card_in_db(card)

@seed_commands.command('all')
def seed():
    seed_cards()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.cli.add_command(seed_commands)

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

def get_random_img():
    random_card = requests.get("https://db.ygoprodeck.com/api/v7/randomcard.php").json()
    cropped_img = f"https://images.ygoprodeck.com/images/cards_cropped/{random_card['id']}.jpg"

    return cropped_img

def get_cards_comments(card):
    all_comments = Comment.query.filter(Comment.card_id == card["id"]).order_by(Comment.id.desc()).all()

    print([comment.to_dict() for comment in all_comments])
    return [comment.to_dict() for comment in all_comments]

def get_users_comments(user_id):
    comments = Comment.query.order_by(Comment.id.desc()).filter(Comment.user_id == user_id).all()

    return [comment.to_dict() for comment in comments]

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
def get_search_bar_options(card_name):
    cards = Card.query.filter(Card.name.ilike(card_name + "%")).limit(10).all()
    return [{"id": card.id, "name": card.name} for card in cards]   

def get_random_card():
    random_card = Card.query.order_by(func.random()).limit(1).first()

    return random_card

def get_recent_comments():
    recent_comments = Comment.query.order_by(Comment.id.desc()).limit(10).all()
    return recent_comments

def get_recent_decks():
    recent_decks = Deck.query.order_by(Deck.id.desc()).limit(10).all()
    return recent_decks

# APP ROUTES ->
@app.route("/")
def home():
    recent_comments = get_recent_comments()
    recent_decks = get_recent_decks()

    return render_template("home.html", recent_comments=recent_comments, recent_decks=recent_decks)

@app.route("/cards/search/page/<int:page_number>", methods=["POST", "GET"])
def search_paginated(page_number):
    card_name = request.form.get("card-name")

    if card_name.lower().startswith("spell:"):
        card_name_updated = card_name.replace("spell:", "")
        paginated_cards = Card.query.filter(Card.type.ilike("%" + "spell" + "%"), Card.name.ilike(card_name_updated + "%")).paginate(page=page_number, per_page=50)
    elif card_name.lower().startswith("monster:"):
        card_name_updated = card_name.replace("monster:", "")
        paginated_cards = Card.query.filter(Card.type.ilike("%" + "monster" + "%"), Card.name.ilike(card_name_updated + "%")).paginate(page=page_number, per_page=50)
    elif card_name.lower().startswith("trap:"):
        card_name_updated = card_name.replace("trap:", "")
        paginated_cards = Card.query.filter(Card.type.ilike("%" + "trap" + "%"), Card.name.ilike(card_name_updated + "%")).paginate(page=page_number, per_page=50)
    else:
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
                return redirect(f"/card/{paginated_cards.items[0].id}")
        return render_template(
            "cards.html", 
            cards=paginated_cards.items, 
            card_name=card_name, 
            page_number=paginated_cards.page, 
            prev=paginated_cards.has_prev, 
            next=paginated_cards.has_next,
            total=paginated_cards.total,
        )

@app.route("/card/<card_id>")
def card(card_id):
    card = Card.query.get(card_id).to_dict()

    sets = get_card_sets(card)
    comments = get_cards_comments(card)

    if "Error" not in card:
        return render_template("card.html", card=card, sets=sets, comments=comments)
    else:
        error = f"{card_id} was not found"
        return render_template("home.html", error=error)

@app.route("/search/names/<card_name>")
def get_options(card_name):
    cards = get_search_bar_options(card_name)
    return cards

#USER ROUTES ->
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/users/create", methods=["POST"])
def create_user():

    hashed_password = generate_password_hash(request.form.get("password"))

    user = User(
        fname=request.form.get('fname'),
        lname=request.form.get('lname'),
        username=request.form.get('username'),
        hashed_password=hashed_password,
        bio=request.form.get('bio'),
    )

    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect("/")


@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return render_template("login.html")

@app.route("/users/login", methods=["POST"])
def login():
    password = request.form.get("password")
    username = request.form.get("username")
    error = "Username or Password is incorrect"
    user = User.query.filter(User.username == username).first()

    if user:
        password_is_correct = user.check_password(password)
        if password_is_correct:
            login_user(user)
            return redirect("/")    
        else:
            return render_template("login.html", error=error) 
    else:
        return render_template("login.html", error=error)       

@app.route("/users/<int:user_id>")
def profile_page(user_id):
    user = User.query.get(user_id)
    comments = get_users_comments(user_id)
    users_decks = user.decks

    return render_template("profile.html", user=user, comments=comments, decks=users_decks)

#COMMENT ROUTES ->
@app.route("/comments", methods=["POST"])
def post_comment():
    card_id = request.form.get("card_id")
    content = request.form.get("content")

    new_comment = Comment(
        user_id=current_user.id,
        card_id=card_id,
        content=content
    )

    db.session.add(new_comment)
    db.session.commit()

    return redirect(f"/card/{card_id}")


#DECK ROUTES ->
@app.route("/users/<int:user_id>/decks")
def users_decks(user_id):
    decks = Deck.query.filter(Deck.user_id == user_id)
    return render_template("users-decks.html", decks=decks)

@app.route("/decks", methods=["POST"])
def create_deck():
    name = request.form.get("name")

    cover_img = get_random_img()

    deck = Deck(
        name=name,
        user_id=current_user.id,
        cover_img=cover_img
    )

    db.session.add(deck)
    db.session.commit()

    return redirect(f"/decks/{deck.id}")

@app.route("/decks/<int:deck_id>", methods=["GET"])
def get_deck(deck_id):
    deck = Deck.query.get(deck_id)
    decklist = deck.get_decklist()

    main_deck_length = 0
    for card in decklist['main_deck']:
        main_deck_length += card["quantity"]

    extra_deck_length = 0
    for card in decklist['extra_deck']:
        extra_deck_length += card["quantity"]

    return render_template("deck.html", deck=deck, decklist=decklist, main_deck_length=main_deck_length, extra_deck_length=extra_deck_length)

@app.route("/decklist/add-quantity/<int:deck_id>/<int:card_id>", methods=["POST"])
def add_card_quantity(deck_id, card_id):
    decklist = DeckList.query.filter(DeckList.card_id==card_id, DeckList.deck_id==deck_id).first()
    decklist.quantity += 1

    db.session.commit()
    return {"response": decklist.quantity}

@app.route("/decklist/del-quantity/<int:deck_id>/<int:card_id>", methods=["POST"])
def del_card_quantity(deck_id, card_id):
    decklist = DeckList.query.filter(DeckList.card_id==card_id, DeckList.deck_id==deck_id).first()
    if decklist.quantity == 1:
        db.session.delete(decklist)
        db.session.commit()
        return {"response": 0}
    else:
        decklist.quantity -= 1
        db.session.commit()
        return {"response": decklist.quantity}


@app.route("/decks/<int:deck_id>/404")
def card_not_found(deck_id):
    deck = Deck.query.get(deck_id)
    decklist = deck.get_decklist()
    return render_template("deck.html", deck=deck, decklist=decklist, error="Card not found")

@app.route("/decklist/<int:deck_id>/<int:card_id>", methods=["POST"])
def add_card_to_decklist(deck_id, card_id):
    card = Card.query.get(card_id)

    if card:
        check_if_exists = DeckList.query.filter(DeckList.card_id==card.id, DeckList.deck_id==deck_id).first()
        if check_if_exists:
            check_if_exists.quantity = check_if_exists.quantity + 1
            db.session.commit()
        else:    
            new_decklist_update = DeckList(card_id=card.id, deck_id=deck_id)
            db.session.add(new_decklist_update)
            db.session.commit()

        return redirect(f"/decks/{deck_id}")
    else:
        error = "Card not found"
        return redirect(f"/decks/{deck_id}/404")
        
@app.route("/decklist/delete", methods=["POST"])
def delete_from_deck():
    card_id = request.form.get("card-id")
    deck_id = request.form.get("deck-id")
    
    decklist = DeckList.query.filter(DeckList.card_id==card_id, DeckList.deck_id==deck_id).first()
    if decklist.quantity > 1:
        decklist.quantity = decklist.quantity - 1
    else:
        db.session.delete(decklist)
    
    db.session.commit()
    
    deck = Deck.query.get(deck_id)
    decklist = deck.get_decklist()
    return redirect(f"/decks/{deck_id}")

@app.route("/card/<card_name>/img")
def get_card_img(card_name):
    card = Card.query.filter(Card.name == card_name).first()
    
    print(card.img_url)

    return {"img_url": card.img_url}

@app.route("/decks/<int:deck_id>/edit", methods=["POST"])
def edit_deck(deck_id):
    deck_name = request.form.get("deck-name")
    deck = Deck.query.get(deck_id)

    deck.name = deck_name
    db.session.commit()

    return redirect(f"/decks/{deck.id}")