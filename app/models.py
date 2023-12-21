# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

# Create a SQLite database engine
engine = create_engine("sqlite:///restaurant.db")

# Declare a base class for declarative models
Base = declarative_base()

# Create all the defined tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session to interact with the database
session = Session()

# Define the Restaurant class
class Restaurant(Base):
    # Define the table name
    __tablename__ = 'restaurants'

    # Define columns for the table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())
    customer_id = Column(Integer(), ForeignKey("customers.id"))

    # Define relationships with other tables
    reviews = relationship('Review', back_populates='restaurant')
    customers = association_proxy('reviews', 'customer', creator=lambda us: Review(customer=us))

    # Class method to get the fanciest restaurant based on price
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    # Method to get all reviews for the restaurant
    def all_reviews(self):
        reviews = self.reviews
        return [review.full_review() for review in reviews]

    # Representation of the object for debugging purposes
    def __repr__(self):
        return f'Restaurant(id={self.id}, name={self.name})'

# Define the Customer class
class Customer(Base):
    # Define the table name
    __tablename__ = "customers"

    # Define columns for the table
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    restaurant_id = Column(Integer(), ForeignKey("restaurants.id"))

    # Define relationships with other tables
    reviews = relationship('Review', back_populates='customer')
    restaurants = association_proxy('reviews', 'restaurant', creator=lambda rst: Review(restaurant=rst))

    # Method to get all reviews left by the customer
    def customer_reviews(self):
        return self.reviews

    # Method to get all restaurants reviewed by the customer
    def customer_restaurants(self):
        return self.restaurants

    # Method to get the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # Method to get the favorite restaurant based on the highest star rating
    def favorite_restaurant(self):
        review_rest = max(self.customer_reviews(), key=lambda a: a.star_rating).customer_restaurants()
        return review_rest

    # Method to add a review for a restaurant
    def add_review(self, restaurant, rating):
        review = Review(
            customer_id=self.id,
            restaurant_id=restaurant.id,
            star_rating=rating
        )
        session.add(review)
        session.commit()

    # Method to delete all reviews for a specific restaurant
    def delete_reviews(self, restaurant):
        delete = [review for review in self.customer_reviews() if review.review_restaurant() == restaurant]

        for review in delete:
            session.delete(review)

        session.commit()

    # Representation of the object for debugging purposes
    def __repr__(self):
        return f'Customer(id={self.id}, first_name={self.first_name}, last_name={self.last_name})\n'

# Define the Review class
class Review(Base):
    # Define the table name
    __tablename__ = "reviews"

    # Define columns for the table
    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    comment = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Define foreign key relationships
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    # Define relationships with other tables
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    # Method to get the customer for this review
    def review_customer(self):
        return self.customer

    # Method to get the restaurant for this review
    def review_restaurant(self):
        return self.restaurant

    # Method to get a full review string
    def full_review(self):
        return f"Review for {self.review_restaurant().name} by {self.review_customer().full_name()}: {self.star_rating} stars."

# Check if the script is being run directly
if __name__ == '__main__':
    # Create a new engine and session
    engine = create_engine("sqlite:///restaurant.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
