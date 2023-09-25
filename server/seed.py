from faker import Faker
from app import app, db  # Import your Flask app and SQLAlchemy db instance
from model import Pizzas, Restaurants, Restaurant_Pizzas  # Import your models
import random

# Your restaurant and pizza data
restaurant_names = [
    "Pizza Paradise",
    "The Crust Factory",
    "Slice of Heaven",
    "Pizza Palace",
    "Mamma Mia Pizzeria",
    "Pizza Planet",
    "Cheesy Delights",
    "Pie Haven",
    "Saucy Slices",
    "Pizza World",
]

pizza_names = [
    "Spicy BBQ",
    "Mediterranean Delight",
    "Seafood Sensation",
    "Veggie Supreme",
    "Sizzling Steakhouse",
    "Mexican Fiesta",
    "Pesto Pleasure",
    "Tropical Bliss",
    "Bacon Bonanza",
    "Gourmet Goat Cheese",
]

with app.app_context():
    fake = Faker()

    # Clear existing data (optional, depending on your needs)
    db.drop_all()
    db.create_all()

    # Populate restaurants
    restaurants = []
    for restaurant in restaurant_names:
        new_restaurant = Restaurants(
            name=restaurant,
            address=fake.address()
        )
        restaurants.append(new_restaurant)
    db.session.add_all(restaurants)
    db.session.commit()
    print("Restaurants successfully populated")

    # Populate pizzas
    pizzas = []
    for pizza in pizza_names:
        new_pizza = Pizzas(
            name=f'{pizza} pizza',
            ingredients=', '.join([' '.join(fake.words(2)) for _ in range(4)])
        )
        pizzas.append(new_pizza)
    db.session.add_all(pizzas)
    db.session.commit()
    print("Pizzas successfully populated")

    # Populate restaurant_pizzas
    restaurant_pizzas = []
    for restaurant in Restaurants.query.all():
        random_pizza_count = random.randint(1, 7)
        for i in range(random_pizza_count):
            new_restaurant_pizza = Restaurant_Pizzas(
                pizza_id=random.randint(1, 10),  # Adjust the range based on your pizza IDs
                restaurant_id=restaurant.id,
                price=random.randint(5, 25)  # Adjust the price range as needed
            )
            restaurant_pizzas.append(new_restaurant_pizza)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    print("Restaurant Pizzas successfully populated")