from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, radius):
        self.id = id
        self.name = name
        self.description = description
        self.radius = radius

# Revisit how to fix formatting of strings in description
planets = [
    Planet(1, "Mercury", "Mercury is the smallest planet in our solar system.",
       "1,516 mi"),
    Planet(2, "Venus", "In addition to being extremely hot, Venus is unusual"\
       " because it spins in the opposite direction of Earth and most other planets.", "3,760.4 mi"),
    Planet(3, "Earth", "Earth is the third planet from the Sun and the only place"\
        " known in the universe where life has originated and found habitability.", "3,958.8 mi"),
    Planet(4, "Mars", "Mars is the fourth planet from the Sun and the third largest"\
        " and massive terrestrial object in the Solar System.", "2,106.1 mi"),
    Planet(5, "Jupiter", "Jupiter is the fifth planet from the Sun and the largest"\
        " in the Solar System.", "43,441 mi"),
    Planet(6, "Saturn", "Saturn is the sixth planet from the Sun and the second-"\
       " largest in the Solar System, after Jupiter.", "36,184 mi"),
    Planet(7, "Uranus", "Uranus is the seventh planet from the Sun and is named"\
        " after Greek sky deity Uranus.", "15,759.2 mi"),
    Planet(8, "Neptune", "Neptune is the eighth planet from the Sun and the" \
       " farthest known planet in the Solar System.", "15,299.4 mi")]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def get_planets():
    result = []
    for planet in planets:
        result.append(dict(
            id = planet.id,
            name = planet.name,
            description = planet.description,
            radius = planet.radius,
        ))
    
    return jsonify(result)

@planet_bp.route("/<id>", methods=["GET"])
def get_planet(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"id {id} is invalid"}, 400))

    for planet in planets:
        if planet.id == id:
            return dict(
                id = planet.id,
                name = planet.name,
                description = planet.description,
                radius = planet.radius,
            )

    abort(make_response({"message":f"planet {id} not found"}, 404))