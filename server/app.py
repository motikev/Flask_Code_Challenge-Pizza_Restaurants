from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from model import db, Pizzas, Restaurant_Pizzas, Restaurants # import the table models


app = Flask(__name__)  # initializes app
app. config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizza.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Flask-Migrate
migrate = Migrate(app, db)

db.init_app(app)

# Initialize Flask-RESTful
api = Api(app) 

# Define a route for the homepage
@app.route("/")
def index():
    return "<h1>Pizza Hut</h1>"

# Define a resource for retrieving restaurant data
class Restaurant(Resource):

    def get(self):
        restaurants = Restaurants.query.all()
        index = []
        for restaurant in restaurants:
            data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            index.append(data)

        return make_response(jsonify(index), 200)

# route for restaurant
api.add_resource(Restaurant, "/restaurants")


# Define a resource for retrieving restaurant data by ID

class RestaurantId(Resource):
    def get(self, id):
        restaurant = Restaurants.query.get(id)
        if restaurant:
            data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": [
                    {
                        "id": pizza.id,
                        # Access the 'name' attribute from the associated Pizza object
                        "name": pizza.pizzas.name,
                        # Access the 'ingredients' attribute from the associated Pizza object
                        "ingredients": pizza.pizzas.ingredients
                    }
                    for pizza in restaurant.respizza
                ],
            }
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)


# Add the RestaurantId resource to the API with a specific endpoint
api.add_resource(RestaurantId, "/resid/<int:id>")

# Define a resource for deleting a restaurant

class Restaurant_Delete(Resource):

    def delete(self, id):

        res_delete = Restaurants.query.filter_by(id=id).first()

        if res_delete:

            for respizza in res_delete.respizza:
                db.session.delete(respizza)
                db.session.commit()
                return make_response("", 204)

        else:
            return make_response(jsonify({"error": "Restaurant not found"}))

# Add the Restaurant_Delete resource to the API with a specific endpoint


api.add_resource(Restaurant_Delete, "/deleteres/<int:id>")

# Define a resource for retrieving pizza data


class Pizza_Get(Resource):

    def get(self):

        pizzas = Pizzas.query.all()
        pizza_dict = []
        for n in pizzas:
            data = {
                "id": n.id,
                "name": n.name,
                "ingredients": n.ingredients
            }

            pizza_dict.append(data)

            return make_response(jsonify(pizza_dict), 200)

 # Add the pizza_get resource to the API with a specific endpoint


api.add_resource(Pizza_Get, "/pizza")


# Define a resource for creating restaurant-pizza associations
class Restaurant_pizza(Resource):

    def post(self):

        data = request.get_json()

        new_data = Restaurant_Pizzas(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )

        db.session.add(new_data)
        db.session.commit()

        return make_response("", 201)

# Add the Restaurant_pizza resource to the API with a specific endpoint


api.add_resource(Restaurant_pizza, "/restaurant_pizzas")


# Run the Flask app
if __name__ == "__main__":
    app.run(port=5555, debug=True)