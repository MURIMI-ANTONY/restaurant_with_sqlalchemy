# Import necessary modules
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import SQLAlchemy models
from models import Restaurant, Review, Customer, Base

# Check if the script is being run directly
if __name__ == "__main__":
    # Initialize Faker for generating fake data
    fake = Faker()

    # Create a SQLite database engine
    engine = create_engine("sqlite:///restaurant.db")

    # Create a session factory
    Session = sessionmaker(bind=engine)

    # Create a session to interact with the database
    session = Session()

    # Lists to store generated instances of Restaurant, Customer, and Review
    restaurants = []
    customers = []
    reviews = []

    # Generate fake data for 50 restaurants
    for i in range(50):
        rest = Restaurant(
            name=fake.unique.company(),
            price=random.randint(5, 100)
        )
        session.add(rest)
        restaurants.append(rest)

    # Generate fake data for 30 customers
    for i in range(30):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(customer)
        customers.append(customer)

    # Generate fake data for 30 reviews
    for i in range(30):
        review = Review(
            star_rating=random.randint(1, 5),
            comment=fake.text(),
            restaurant=random.choice(restaurants),
            customer=random.choice(customers)
        )
        session.add(review)
        reviews.append(review)

    # Commit the changes to the database
    session.commit()

    # Close the session
    session.close()
