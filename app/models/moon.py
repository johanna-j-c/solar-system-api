from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    size = db.Column(db.String)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", back_populates="moons")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desription": self.description,
            "size": self.size
        }
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            name = data_dict["name"],
            description = data_dict["description"],
            size = data_dict["size"]
        )