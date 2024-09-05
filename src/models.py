from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)




    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": [favorite.serialize() for favorite in self.favorites]
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    
    user = db.relationship("User", backref="favorites")
    planet = db.relationship("Planet", backref="favorites")
    character = db.relationship("Character", backref="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        } 
    

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    terrain = db.Column(db.String(255))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "population": self.population
        } 
    
class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    eye_color = db.Column(db.String(255))


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "eye_color": self.eye_color
        } 
