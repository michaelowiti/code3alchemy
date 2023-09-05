from sqlalchemy import String, Integer, Column, create_engine, MetaData, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.associationproxy import association_proxy



convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


engine = create_engine('sqlite:///storage.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    created_at = Column (DateTime(), server_default=func.now())
    updated_at = Column (DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='customer_review', cascade='all, delete-orphan')
    restaurants = association_proxy('reviews', 'restaurant_review',
        creator=lambda rs: Review(restaurant=rs))
    

    # def given_name(self):
    #      return self.first_name
    
    # def family_name(self):
    #      return self.last_name
    
    # def full_name(self):
    #      fullname = self.first_name + " " + self.last_name
    #      return fullname
    
    # @classmethod
    # def all(cls):
    #    return cls.all_customers 
    
    
    def __repr__(self):

        return f'Customer(id={self.id}, ' + \
            f'first_name={self.first_name}, ' + \
            f'last_name={self.last_name})'
    
    #  methods
    # returns a collection of all the reviews that the Customer has left
    # def all_reviews(self):
    #     return self.reviews
        # return session.query(Review).filter_by(customer_id=self.id).all()

    # returns a collection of all the restaurants that the Customer has reviewed
    def all_restaurants(self):
        if not self.restaurants:
            return "This customer has not left any restaurant reviews."
        return self.restaurants

    # returns the full name of the customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    # returns the restaurant instance that has the highest star rating from this customer
    def favorite_restaurant(self):

        reviews = self.all_reviews()

        if not reviews:
            return "Customer has no reviews for any restaurant."
        
        highest_rating_review = max(reviews, key=lambda review: review.star_rating)
        return session.query(Restaurant).filter_by(id=highest_rating_review.restaurant_id).first()
    
    # creates a new review for the restaurant with the given restaurant_id
    def add_review(self, restaurant, rating):

        if isinstance(rating, int):
            review = Review(
                star_rating = rating,
                restaurant_id = restaurant.id,
                customer_id = self.id,
                )
            
            self.reviews.append(review)

            session.add(review)
            session.commit()

            print(f"New review added successfully.")
            
            return review
        else:
            return "Rating must be an integer."
        
    # removes all of that customer reviews for a restaurant
    def delete_reviews(self, restaurant):
        
        reviewed_restaurants = self.restaurants

        if restaurant in reviewed_restaurants:
            for res in reviewed_restaurants:
                if res.id == restaurant.id:
                    session.query(Review).filter_by(restaurant_id=res.id).delete()
                
                session.commit()
            return "Restaurant review deleted successfully."        
        else:
            return "Review not found."
    
    # def restaurants(self):
    #     the_reviews = session.query(Review).all()
    #     restaurants_reviewed = []
    #     for that_review in the_reviews:
    #         if that_review.restaurant_customer == self.first_name:
    #             restaurants_reviewed.append(that_review.restaurant) 
    #         else:
    #             return 'restaurant not found'
    #     return(set(restaurants_reviewed))
         
    
    # def add_review(self, restaurant_, rating):
    #     new = Review(restaurant_name =restaurant_, customer_rating=rating, restaurant_customer= self.first_name)
    #     session.add(new)
    #     session.commit()
    #     session.close()
         
    # def num_reviews(self): 
    #     number_reviews = session.query(Review).filter(Review.restaurant_customer ==self.first_name).count()              
    #     return number_reviews
    # @classmethod
    # def find_by_name(cls, name):
    #     for customer in cls.all_customers:
    #         if f'{customer.first_name} {customer.last_name}' == name:
    #             return customer.first_name
    #         else:
    #             return "customer not found"  
                          
    # @classmethod      
    # def find_all_given_name(cls, name):
    #     for customer in cls.all_customers:
    #         if customer.first_name == name:
    #             return customer.first_name
    #         else:
    #             return 'Names not available.'
            

#Restaurant


class Restaurant(Base):
    __tablename__= 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String(),index =True)
    price = Column (Integer())
    created_at = Column (DateTime(), server_default=func.now())
    updated_at = Column (DateTime(), onupdate=func.now())

    reviews = relationship('Review', back_populates='restaurant_review', cascade='all, delete-orphan')
    customers = association_proxy('reviews', 'customer_review',
        creator=lambda cus: Review(customer=cus))



    def __repr__(self):

        return f'Restaurant(id={self.id}, ' + \
            f'name={self.name}, ' + \
            f'price={self.price})'
    
    # Restaurant instance methods
    # returns a collection of all the reviews for the Restaurant
    def all_reviews(self):
        return session.query(Review).filter_by(restaurant_id=self.id).all()
    
    # returns a collection of all the customers who reviewed the Restaurant
    def all_customers(self):
        # return list({review.customer_review for review in self.reviews})
        return session.query(Customer).distinct().join(Review).filter(Review.restaurant_review == self).all()

    # returns one restaurant instance for the restaurant that has the highest price
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    # returns a list of formatted strings with all the reviews for this restaurant
    def all_reviews_formatted(self):
        review_strings = []
        for review in self.reviews:
            review_string = f"Review for {self.name} by {review.customer_review.first_name} {review.customer_review.last_name}: {review.star_rating} stars."
            review_strings.append(review_string)
        return review_strings


    # def __init__(self, restaurant_name):
    #     self.restaurant_name = restaurant_name

    # def name(self):
    #     return self.restaurant_name
    
    # def reviews(self):
    #     the_reviews = session.query(Review).all() 
    #     for that_review in the_reviews:
    #         if that_review.restaurant_name == self.restaurant_name:
    #             return that_review
    #         else:
    #             return 'restaurant not found'

    # def customers(self):
    #     the_reviews = session.query(Review).all()
    #     customer_who_reviewed = []
    #     for that_review in the_reviews:
    #         if that_review.restaurant_name == self.restaurant_name:
    #             customer_who_reviewed.append(that_review.restaurant_customer) 
    #         else:
    #             return 'restaurant not found'
    #     return(set(customer_who_reviewed))    
                
    # def  average_star_rating(self):
    #     the_reviews = session.query(Review).filter(self.restaurant_name)
    #     sum_reviews = 0
    #     number_counts = 0
    #     for that_review in the_reviews:
    #         if that_review.restaurant_name == self.restaurant_name:
    #             sum_reviews = sum_reviews + that_review.customer_rating
    #             number_counts += 1
    #         else:
    #             return "No ratings found"
    #     average_rating = sum_reviews // number_counts
    #     return average_rating      


#Reviews

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key = True)
    restaurant_id = Column(Integer())
    customer_id = Column(Integer())
    star_rating = Column(Integer())
    created_at = Column (DateTime(), server_default=func.now())
    updated_at = Column (DateTime(), onupdate=func.now())
    

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    restaurant_review = relationship('Restaurant', back_populates='reviews')
    customer_review = relationship('Customer', back_populates='reviews')

    # all_reviews = []
    # def __init__(self, restaurant, restaurant_customer, customer_rating):
    #     self.restaurant_ = restaurant
    #     self.restaurant_customer = restaurant_customer
    #     self.customer_rating = customer_rating
    #     Review.all_reviews.append(self)

    # def rating(self):
    #     return self.customer_rating
    
    # @classmethod
    # def all(cls):
    #     for review in cls.all_reviews:
    #         return review

    # def customer(self):
    #     reviewing_customers = session.query(Customer).all()
    #     for theCustomer in reviewing_customers:
    #         if theCustomer.first_name == self.restaurant_customer:
    #             return theCustomer
    #         else:
    #             return "customer not found"



    def __repr__(self):

        return f'Review(id={self.id}, ' + \
            f'star_rating={self.star_rating}, ' + \
            f'restaurant_id={self.restaurant_id})'

    # Review instance methods
    # returns the Customer instance for this review
    def customer(self):
        return session.query(Customer).filter_by(id=self.customer_id).first()
    
    # returns the restaurant instance for this review
    def restaurant(self):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()

    # return a custom string formatted review
    def full_review(self):
        restaurant_name = self.restaurant.name
        customer_name = f'{self.customer.first_name} {self.customer.last_name}'
        star_rating = self.star_rating
        return f'Review for {restaurant_name} by {customer_name}: {star_rating} stars'
    

if __name__ == '__main__':

    # Instances for testing
    restaurant1 = session.query(Restaurant).first()
    restaurant_x = session.query(Restaurant).filter_by(id=18).first()

    customer1 = session.query(Customer).first()
    customer_x = session.query(Customer).filter_by(id=4).first()
    # customer2_reviews = session.query(Review).filter_by(customer_id=2).all()
   
    review1 = session.query(Review).first()
            
    # def restaurant(self):
    #     restaurant_reviewed = session.query(Restaurant).all()
    #     for theRestaurant in restaurant_reviewed:
    #         if theRestaurant.restaurant_name == self.restaurant_:
    #             return theRestaurant
    #         else:
    #             return 'The restaurant not found'


    #instance trials

# restaurant1=session.query(Restaurant).first()
# print(restaurant1.name)
                
# customer1 = session.query(Customer).first()
# review2=session.query(Review).first()
# # print(customer1.first_name)
# print(review2.full_review())
    
#print(restaurant1.all_reviews_formatted())
           
    


    

         
     
           