"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound

from sqlalchemy import null, true
from service.models import Shopcart, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/shopcarts"
)

######################################################################
#  Shopcart   M O D E L   T E S T   C A S E S
######################################################################
class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        # app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_repr(self):
        """ Test __repr__ """
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        res = shopcart.__repr__()
        logging.debug(shopcart)
        self.assertEqual(res, "<Shopcart for user 0>")

   
    def test_create_a_shopcart(self):
        """Create a shopcart and assert that it exists"""
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        logging.debug(shopcart)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.user_id, 0)
        self.assertEqual(shopcart.item_id, 0)
        self.assertEqual(shopcart.item_name, "rings")
        self.assertEqual(shopcart.quantity, 2)
        self.assertEqual(shopcart.price, 1000)


    def test_add_a_shopcart(self):
        """ Test create a Shopcart with no item, add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        logging.debug(shopcart)
        shopcart.create()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        
    def test_update_a_shopcart_add_item(self):
        """ Update a Shopcart, change item quantity"""
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        shopcart.create()
        logging.debug(shopcart)
        # Change it and save it
        shopcart.quantity = 3
        shopcart.save()
        # Fetch it back and make sure the user id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        self.assertEqual(shopcarts[0].user_id, 0)
        self.assertEqual(shopcarts[0].item_name, "rings")
        self.assertEqual(shopcarts[0].quantity, 3)
        

    def test_delete_a_shopcart(self):
        """ Delete a Shopcart"""
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        logging.debug(shopcart)
        # delete the shopcart and make sure it isn't in the database
        shopcart.delete()
        self.assertEqual(len(Shopcart.all()), 0)


    def test_serialize_a_shopcart(self):
        """Test serialization of a Shopcart"""
        shopcart = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        data = shopcart.serialize()
        logging.debug(shopcart)
        self.assertNotEqual(data, None)
        self.assertIn("user_id", data)
        self.assertEqual(data["user_id"], shopcart.user_id)
        self.assertIn("item_id", data)
        self.assertEqual(data["item_id"], shopcart.item_id)
        self.assertIn("item_name", data)
        self.assertEqual(data["item_name"], shopcart.item_name)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], shopcart.quantity)
        self.assertIn("price", data)
        self.assertEqual(data["price"], shopcart.price)


    def test_deserialize_a_shopcart(self):
        """Test deserialization of a Shopcart"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : 20.5}
        shopcart = Shopcart()
        logging.debug(shopcart)
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.item_id, 2)
        self.assertEqual(shopcart.item_name, "bottle")
        self.assertEqual(shopcart.quantity, 2)
        self.assertEqual(shopcart.price, 20.5)

    
    def test_deserialize_missing_data(self):
        """Test deserialization of a Shopcart with missing data"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_bad_data(self):
        """Test deserialization of a Shopcart with missing data"""
        data = "This is not a dictionary"
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    
    def test_find(self):
        """ Test Finds a Shopcart-Item by user id, item id """
        shopcart1 = Shopcart(user_id = 0, item_id = 0, item_name = "rings", quantity = 2, price = 1000)
        shopcart2 = Shopcart(user_id = 1, item_id = 1, item_name = "bottle", quantity = 1, price = 20.5)
        shopcart3 = Shopcart(user_id = 2, item_id = 2, item_name = "phone", quantity = 1, price = 666)
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        # make sure they got saved
        self.assertEqual(len(Shopcart.all()), 3)
        # find the second shopcart in the list
        shopcart = Shopcart.find(shopcarts[1].user_id, shopcarts[1].item_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, shopcarts[1].user_id)
        self.assertEqual(shopcart.item_id, shopcarts[1].item_id)
        self.assertEqual(shopcart.item_name, shopcarts[1].item_name)
        self.assertEqual(shopcart.quantity, shopcarts[1].quantity)
        self.assertEqual(shopcart.price, shopcarts[1].price)


    # def test_find_or_404_not_found(self):
    #     """Test Find or return 404 found"""
    #     self.assertRaises(NotFound, Shopcart.find_or_404, 0)
    
