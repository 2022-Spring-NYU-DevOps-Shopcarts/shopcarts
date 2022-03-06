"""
Models for Shopcart

All of the models are stored in this module

Attributes Explanations:

id: primary key for item
user_id: a user id, primary key for shopcart, foreign key for item
name: name of a shopcart
item_name: name of an item
quantity: quantity of an item
price: price of an item
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Item(db.Model):
    """
    Class that represents an item
    """
    app = None
    # Item Table Schema
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('shopcart.user_id'), nullable=False)
    item_name = db.Column(db.String(63))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    

    def __repr__(self):
        return "<Item %s, quantity=[%s], price=[%s]>" % (self.item_name, self.quantity, self.price)

    def serialize(self):
        """ Serializes an item into a dictionary """
        return {"item_name": self.item_name, 
        "quantity": self.quantity,
        "price": self.price,
        "id": self.id,
        "user_id": self.user_id
        }

    def deserialize(self, data):
        """
        Deserializes an item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.user_id = data["user_id"]
            self.item_name = data["item_name"] + ""
            self.quantity = data["quantity"]
            self.price = data["price"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid item: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid item: body of request contained bad or no data"
            )
        return self

    


class Shopcart(db.Model):
    """
    Class that represents a shopcart
    """

    app = None

    # Shopcart Table Schema
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    items = db.relationship('Item', backref='item', cascade="all, delete", lazy=True)


    def __repr__(self):
        return "<Shopcart %r id=[%s]>" % (self.name, self.user_id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating %s", self.name)
        # self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()
    
    def save(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Shopcart from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"user_id": self.user_id, 
        "name": self.name,
        "items": [item.serialize() for item in self.items]
        }

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"] + ""
            self.user_id = data["user_id"]
            self.items = data["items"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data"
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
        """ Returns all of the Shopcarts in the database """
        logger.info("Processing all Shopcarts")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Shopcart by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Shopcart by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Shopcarts with the given name

        Args:
            name (string): the name of the Shopcarts you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
