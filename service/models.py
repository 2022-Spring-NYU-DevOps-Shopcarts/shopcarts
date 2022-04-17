"""
Models for Shopcart

All of the models are stored in this module

Attributes Explanations:

item_id: an item id
user_id: a user id, primary key for shopcart
user_id + item_id serves as the compound primary key in our Shopcart-Item table
item_name: name of an item
quantity: quantity of an item
price: price of an item
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

    


class Shopcart(db.Model):
    """
    Class that represents a shopcart
    """

    app = None

    # Shopcart-Item Table Schema
    user_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(63))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    hold = db.Column(db.Boolean)


    def __repr__(self):
        return "<Product %s in Shopcart for user %s>" % (self.item_id, self.user_id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating shopcart for user %s", self.user_id)
        db.session.add(self)
        db.session.commit()
    
    def save(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving shopcart for user %s", self.user_id)
        db.session.commit()

    def delete(self):
        """ Removes a Shopcart from the data store """
        logger.info("Deleting shopcart for user %s", self.user_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"user_id": self.user_id, 
            "item_id": self.item_id,
            "item_name": self.item_name,
            "quantity": self.quantity,
            "price": self.price,
            "hold": self.hold}
        

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if isinstance(data["user_id"], int):
                self.user_id = data["user_id"]
            else:
                raise DataValidationError(
                    "Invalid type for int [user_id]: "
                    + str(type(data["user_id"]))
                )
            if isinstance(data["item_id"], int):
                self.item_id = data["item_id"]
            else:
                raise DataValidationError(
                    "Invalid type for int [item_id]: "
                    + str(type(data["item_id"]))
                )

            self.item_name = data["item_name"] + ""
            if isinstance(data["quantity"], int):
                self.quantity = data["quantity"]
            else:
                raise DataValidationError(
                        "Invalid type for int [quantity]: "
                        + str(type(data["quantity"]))
                )
            if isinstance(data["price"], float) or isinstance(data["price"], int):
                self.price = data["price"]
            else:
                raise DataValidationError(
                        "Invalid type for float [price]: "
                        + str(type(data["price"]))
                )
            if 'hold' in data:
                if isinstance(data["hold"], bool):
                    self.hold = data["hold"]
                else:
                    raise DataValidationError(
                            "Invalid type for bool [hold]: "
                            + str(type(data["hold"]))
                    )
            else:
                self.hold = False
                
        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart item: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart item: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Shopcart items in the database """
        logger.info("Processing all Shopcart items")
        return cls.query.all()
    
    @classmethod
    def all_shopcart(cls):
        """ Returns all of the non-empty Shopcarts in the database """
        logger.info("Processing all Shopcarts")
        return cls.query.with_entities(cls.user_id).distinct().all()
    
    @classmethod
    def find_shopcart(cls, user_id):
        """ Finds a shopcart (including items it has) by user_id """
        logger.info("Processing lookup for user id %s...", user_id)
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def find_shopcart_or_404(cls, user_id):
        """ Finds a shopcart (first item if found) by user_id """
        logger.info("Processing lookup for user id %s...", user_id)
        return cls.query.filter(cls.user_id == user_id).first_or_404()
    

    @classmethod
    def find_item(cls, user_id, item_id):
        """ Finds an item by user_id and item_id """
        logger.info("Processing lookup for user id %s item id %s...", user_id, item_id)
        return cls.query.filter((cls.user_id == user_id) & (cls.item_id == item_id)).first()


    @classmethod
    def find_item_or_404(cls, user_id, item_id):
        """ Find an item by user_id and item_id """
        logger.info("Processing lookup or 404 for user id %s item id %s...", user_id, item_id)
        return cls.query.filter((cls.user_id == user_id) & (cls.item_id == item_id)).first_or_404()

