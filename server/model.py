from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Initialize SQLAlchemy
db = SQLAlchemy()


class Pizzas(db.Model):
    __tablename__ = "pizza"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

 # Define the relationship with Restaurant_Pizzas
    respizza = db.relationship(
        "Restaurant_Pizzas", back_populates="pizzas", lazy=True)

  # Define a representation for Pizzas

    def __repr__(self):
        return f"Pizzas(id={self.id}, name={self.name}, ingredients{self.ingredients})"

# Define the Restaurants model


class Restaurants(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)

 # Defines the relationship with Restaurant_Pizzas
    respizza = db.relationship(
        "Restaurant_Pizzas", back_populates="restaurants", lazy=True)

# Validation for the 'name' field
    @validates("name")
    def validate_name(self, key, name):

        names = db.session.query(Restaurants.name).all()

        if len(name) > 50:
            raise ValueError("Must have a name less than 50 words")

        elif name in names:
            raise ValueError("Must have a unique name")

        return name

 # Define a representation for Restaurants
    def __repr__(self):
        return f"Restaurant(id={self.id}, name={self.name}, address={self.address})"

# Define the Restaurant_Pizzas model


class Restaurant_Pizzas(db.Model):
    __tablename__ = "respizza"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship(
        "Restaurants", back_populates="respizza", lazy=True)

    # Define the relationship with Pizzas
    pizzas = db.relationship("Pizzas", back_populates="respizza", lazy=True)

 # Validation for the 'price' field
    @validates("price")
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price Must Be Between 1 and 30")

        return price

  # Define a representation for Restaurant_Pizzas
    def __repr__(self):
        return f"Restaurant_Pizzas(id={self.id}, price={self.price})"