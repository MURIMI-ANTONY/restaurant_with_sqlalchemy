from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine("sqlite:///restaurant.db")
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id=Column(Integer(),primary_key = True)
    name =Column(String())
    price = Column(Integer())
    customer_id = Column(Integer(),ForeignKey("customers.id"))

    reviews = relationship('Review', back_populates='restaurant')
    customers = association_proxy('reviews', 'customer',
        creator=lambda us: Review(customer=us))
    
    def restaurant_reviews(self):
        return self.reviews
    
    def restaurant_customers(self):
        return self.customers
    
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        reviews = self.reviews
        return [review.full_review() for review in reviews]

    def __repr__(self):
        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name})'
    

class Customer(Base):
    __tablename__ ="customers"

    id=Column(Integer(),primary_key =True)
    first_name= Column(String())
    last_name = Column(String())
    restaurant_id =Column(Integer(),ForeignKey("restaurants.id"))

    reviews = relationship('Review', back_populates='customer')
    restaurants = association_proxy('reviews', 'restaurant',
        creator=lambda rst: Review(restaurant=rst))
    
    def customer_reviews(self):
        return self.reviews
    
    def customer_restaurants(self):
        return self.restaurants
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def favorite_restaurant(self):
        review_rest =max(self.customer_reviews(),key=lambda a:a.star_rating).customer_restaurants()
        return review_rest
    
    def add_review(self,restaurant,rating):
        review = Review(
            customer_id=self.id,
            restaurant_id=restaurant.id,
            star_rating=rating)
        
        
        session.add(review)
        session.commit()

    def delete_reviews(self,restaurant):
        delete = [review for review in self.customer_reviews() if review.review_restaurant() == restaurant]

        for review in delete:
            session.delete(review)

        session.commit()

    def __repr__(self):
        return f'Customer(id={self.id}, ' + \
            f'first_name={self.first_name}, ' + \
            f'last_name={self.last_name}'+')\n'
    

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())
    comment = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    # Define the relationship properties
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def review_customer(self):
        return self.customer
    
    
    def review_restaurant(self):
        return self.restaurant
    
    def full_review(self):
        return f"Review for {self.review_restaurant().name} by {self.review_customer().full_name()}: {self.star_rating} stars."

fr= session.query(Review).first().customer
first_customer = session.query(Customer).first().restaurants
# first_customer_reviews = first_customer.reviews
# first_customer_restaurants = first_customer.restaurants()
print(fr)


if __name__ == '__main__':
    engine = create_engine("sqlite:///restaurant.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
