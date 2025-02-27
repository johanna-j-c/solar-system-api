import pytest
from app import create_app, db
from flask.signals import request_finished
from app.models.planet import Planet


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_planet(app):
    # Arrange
    planet = Planet(
        name="Mercury",
        description="Mercury is the smallest planet in our solar system.",
        radius="1,516 mi"
    )

    db.session.add(planet)
    db.session.commit()
    return planet

@pytest.fixture
def multiple_planets(app):
    # Arrange
    planet1 = Planet(
        name="Venus",
        description="Venus is extremely hot.",
        radius="3,760.4 mi"
    )
    planet2 = Planet(
        name="Earth",
        description="Earth is the third planet from the Sun.",
        radius="3,958.8 mi"
    )

    planets = [planet1, planet2]

    db.session.add_all(planets)
    db.session.commit()
    return planets