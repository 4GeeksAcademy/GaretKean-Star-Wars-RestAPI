"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200



@app.route('/people', methods=['GET'])
def all_people():
    people = Character.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None :
        raise APIException("person not found", status_code = 404)
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def all_planet():
    planets = Planet.query.all()
    all_planets = [planet.serialize() for planet in planets] 
    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None :
        raise APIException("planet not found", status_code = 404)
    return jsonify(planet.serialize()), 200

@app.route("/users/favorites", methods=["GET"])
def get_all_favorites():
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    
    favorites = Favorite.query.filter_by(user_id = user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorites), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_to_favorites(people_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    character = Character.query.get(people_id)
    if character is None:
        raise APIException("Person not found", status_code=404) 
    favorite = Favorite(name = character.name, user_id = user_id, character_id = people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite people added successfully"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_to_favorites(planet_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404) 
    favorite = Favorite(name = planet.name, user_id = user_id, planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])

def delete_character(people_id):
    user_id = request.args.get("user_id")
    favorite = Favorite.query.filter_by(user_id = user_id, character_id = people_id).first()
    if favorite is None:
        raise APIException("Favorite people not found", status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite people removed successfully"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])

def delete_planet(planet_id):
    user_id = request.args.get("user_id")
    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favorite is None:
        raise APIException("Favorite planet not found", status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet removed successfully"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
