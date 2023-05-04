from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

# class Planet:
#     def __init__(self, id, name, description, radius):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.radius = radius

#     def make_planet_dict(self):
#         return dict(
#             id = self.id,
#             name = self.name,
#             description = self.description,
#             radius = self.radius,
#         )

# planets = [
#     Planet(1, "Mercury", "Mercury is the smallest planet in our solar system.",
#        "1,516 mi"),
#     Planet(2, "Venus", "In addition to being extremely hot, Venus is unusual"\
#        " because it spins in the opposite direction of Earth and most other planets.", "3,760.4 mi"),
#     Planet(3, "Earth", "Earth is the third planet from the Sun and the only place"\
#         " known in the universe where life has originated and found habitability.", "3,958.8 mi"),
#     Planet(4, "Mars", "Mars is the fourth planet from the Sun and the third largest"\
#         " and massive terrestrial object in the Solar System.", "2,106.1 mi"),
#     Planet(5, "Jupiter", "Jupiter is the fifth planet from the Sun and the largest"\
#         " in the Solar System.", "43,441 mi"),
#     Planet(6, "Saturn", "Saturn is the sixth planet from the Sun and the second-"\
#        " largest in the Solar System, after Jupiter.", "36,184 mi"),
#     Planet(7, "Uranus", "Uranus is the seventh planet from the Sun and is named"\
#         " after Greek sky deity Uranus.", "15,759.2 mi"),
#     Planet(8, "Neptune", "Neptune is the eighth planet from the Sun and the" \
#        " farthest known planet in the Solar System.", "15,299.4 mi")]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    try:
        new_planet = Planet.from_dict(request_body)

        db.session.add(new_planet)
        db.session.commit()

        message = f"Planet {new_planet.name} successfully created."

        return make_response(jsonify(message), 201)
    except KeyError as e:
        abort(make_response({"message": f"Missing required value {e}"}, 400))
        

@planet_bp.route("", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    results = [planet.to_dict() for planet in planets]
    
    return jsonify(results)

def validate_planet(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} is invalid"
        abort(make_response({"message": message}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} {model_id} is not found"
        abort(make_response({"message": message}, 404))

    return model

@planet_bp.route("/<id>", methods=["GET"])
def get_planet(id):
    planet = validate_planet(Planet, id)

    return planet.to_dict()

@planet_bp.route("/<id>", methods=["PUT"])
def update_planet(id):
    planet_data = request.get_json()
    planet_to_update = validate_planet(Planet, id)

    planet_to_update.name = planet_data["name"]
    planet_to_update.description = planet_data["description"]
    planet_to_update.radius = planet_data["radius"]

    db.session.commit()
    return make_response(jsonify(f"Planet {planet_to_update.name} updated"), 200)

@planet_bp.route("/<id>", methods=["DELETE"])
def delete_planet(id):
    planet_to_delete = validate_planet(Planet, id)

    db.session.delete(planet_to_delete)
    db.session.commit()

    return make_response(jsonify(f"Planet {planet_to_delete.name} deleted"), 200)