from app import db
from app.models.planet import Planet
from app.models.moon import Moon
from flask import Blueprint, jsonify, abort, make_response, request

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
    name_query = request.args.get("name")
    radius_query = request.args.get("radius")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    elif radius_query:
        planets = Planet.query.filter_by(radius=radius_query)
    else:
        planets = Planet.query.all()
    
    results = [planet.to_dict() for planet in planets]
    
    return jsonify(results)

def validate_model(cls, model_id):
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
    planet = validate_model(Planet, id)

    return planet.to_dict()

@planet_bp.route("/<id>", methods=["PUT"])
def update_planet(id):
    planet_data = request.get_json()
    planet_to_update = validate_model(Planet, id)

    planet_to_update.name = planet_data["name"]
    planet_to_update.description = planet_data["description"]
    planet_to_update.radius = planet_data["radius"]

    db.session.commit()
    return make_response(jsonify(f"Planet {planet_to_update.name} updated"), 200)

@planet_bp.route("/<id>", methods=["DELETE"])
def delete_planet(id):
    planet_to_delete = validate_model(Planet, id)

    db.session.delete(planet_to_delete)
    db.session.commit()

    return make_response(jsonify(f"Planet {planet_to_delete.name} deleted"), 200)

# # Planet routes for accessing moon
@planet_bp.route("/<id>/moons", methods=["POST"])
def create_moon(id):
    request_body = request.get_json()
    planet = validate_model(Planet, id)
    try:
        new_moon = Moon.from_dict(request_body)
        new_moon.planet = planet

        db.session.add(new_moon)
        db.session.commit()

        message = f"Moon {new_moon.name} successfully created"

        return make_response(jsonify(message), 201)
    except KeyError as e:
        abort(make_response({"message": f"Missing required value {e}"}, 400))
    
@planet_bp.route("/<id>/moons", methods=["GET"])
def read_moons(id):
    planet = validate_model(Planet, id)

    moons_response = []
    for moon in planet.moons:
        moons_response.append(moon.to_dict())
    return jsonify(moons_response)