from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Review, Customer,Base

if __name__ == "__main__":
    fake = Faker()
    engine = create_engine("sqlite:///restaurant.db")
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    restaurants = []
    for i in range(50):
        rest = Restaurant(
            name=fake.unique.company(),
            price=random.randint(5, 100)
        )
        session.add(rest)
        restaurants.append(rest)

    customers = []
    for i in range(30):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(customer)
        customers.append(customer)

    reviews = []
    for i in range(30):
        review = Review(
            star_rating=random.randint(1, 5),
            comment=fake.text(),
            restaurant=random.choice(restaurants),
            customer=random.choice(customers)
        )
        session.add(review)
        reviews.append(review)

    session.commit()
    session.close()
