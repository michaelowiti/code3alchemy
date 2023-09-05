from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    fake = Faker()

    # Sample 20 restaurants in Kenya
    ke_restaurants = [
        "Carnivore Restaurant",
        "Talisman Restaurant",
        "Mama Oliech Restaurant",
        "Nyama Mama",
        "Habesha Restaurant",
        "The Talisman",
        "Java House",
        "Artcaffe",
        "Cafe Deli",
        "Mama Rocks Gourmet Burgers",
        "About Thyme Restaurant",
        "Cafe Maghreb",
        "Lord Erroll Gourmet Restaurant",
        "Que Pasa Bar & Bistro",
        "Sankara Nairobi, Sarabi Rooftop Bar",
        "Anghiti Restaurant",
        "Seven Seafood & Grill",
        "Zen Garden",
        "Hashmi BBQ",
        "Le Palanka"
    ]

    restaurants = []
    for i in range(20):
        restaurant = Restaurant(
            name = random.choice(ke_restaurants),
            price = random.randint(100, 1000)
        )

        session.add(restaurant)
        session.commit()

        restaurants.append(restaurant)

    customers = []
    for i in range (60): # Generate 60 fake customers
        customer = Customer(
            first_name = fake.first_name(),
            last_name = fake.last_name()                        
        )

        session.add(customer)
        session.commit()

        customers.append(customer)

    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(0, 10)): # Generate between 0 and 10 reviews per restaurant
            customer = random.choice(customers)  # Choose a random customer in the list
            restaurant = random.choice(restaurants)  # Choose a random restaurant in the list
            review = Review(
                star_rating=random.randint(1, 10),
                customer_id=customer.id,  # Set the customer_id for the review
                restaurant_id=restaurant.id, # Set the restaurant_id for the review
            )
            reviews.append(review)

    session.bulk_save_objects(reviews)
    session.commit()
    session.close()