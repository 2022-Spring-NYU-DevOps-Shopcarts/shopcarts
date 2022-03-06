"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound

from sqlalchemy import null, true
from service.models import Shopcart, Item, DataValidationError, db
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
        test_obj = Shopcart()
        res = test_obj.__repr__()
        self.assertEqual(res, "<Shopcart None id=[None]>")

   
    def test_create_a_shopcart(self):
        """Create a shopcart and assert that it exists"""
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.user_id, 0)
        self.assertEqual(shopcart.name, "Alice")
        self.assertEqual(shopcart.items, [])

    def test_add_a_shopcart(self):
        """ Test create a Shopcart with no item, add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        shopcart.create()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        
    def test_update_a_shopcart_add_item(self):
        """ Update a Shopcart, add a new item to shopcart"""
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        shopcart.create()
        logging.debug(shopcart)
        # Change it and save it
        item1 = Item(item_name="bottle", quantity=1, price=20.5)
        shopcart.items.append(item1)
        shopcart.update()
        # Fetch it back and make sure the user id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        self.assertEqual(shopcarts[0].user_id, 0)
        self.assertEqual(shopcarts[0].items[0].item_name, "bottle")
        self.assertEqual(shopcarts[0].items[0].quantity, 1)
        self.assertEqual(shopcarts[0].items[0].price, 20.5)
        
    def test_update_a_shopcart_remove_item(self):
        """ Update a Shopcart, remove an item to shopcart"""
        item1 = Item(item_name="bottle", quantity=1, price=20.5)
        shopcart = Shopcart(user_id = 0,name="Alice", items = [item1])
        shopcart.create()
        # Change it and save it
        shopcart.items.pop()
        shopcart.update()
        # Fetch it back and make sure the user id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        self.assertEqual(shopcarts[0].user_id, 0)
        self.assertEqual(len(shopcarts[0].items), 0)

    def test_delete_a_shopcart(self):
        """ Delete a Shopcart"""
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        # delete the shopcart and make sure it isn't in the database
        shopcart.delete()
        self.assertEqual(len(Shopcart.all()), 0)

    def test_serialize_a_shopcart(self):
        """Test serialization of a Shopcart"""
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        data = shopcart.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("user_id", data)
        self.assertEqual(data["user_id"], shopcart.user_id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], shopcart.name)
        self.assertIn("items", data)
        self.assertEqual(data["items"], shopcart.items)

    def test_deserialize_a_shopcart(self):
        """Test deserialization of a Shopcart"""
        data = {"user_id" : 1, "name" : "Bob", "items" : []}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.name, "Bob")
        self.assertEqual(shopcart.items, [])
    
    def test_deserialize_missing_data(self):
        """Test deserialization of a Shopcart with missing data"""
        data = {"user_id": 1, "name" : "Bob"}
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of a Shopcart with missing data"""
        data = "This is not a dictionary"
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)
    
    def test_deserialize_wrong_field_type(self):
        data = {"user_id": "1", "name" : "Bob"}
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)
    
    def test_find_shopcart(self):
        """ Test Finds a Shopcart by it's ID """
        shopcart1 = Shopcart(user_id = 0,name="Alice", items = [])
        shopcart2 = Shopcart(user_id = 1, name="Bob", items = [])
        shopcart3 = Shopcart(user_id = 2, name = "Kevin", items = [])
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        # make sure they got saved
        self.assertEqual(len(Shopcart.all()), 3)
        # find the second shopcart in the list
        shopcart = Shopcart.find(shopcarts[1].user_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, shopcarts[1].user_id)
        self.assertEqual(shopcart.name, shopcarts[1].name)
        self.assertEqual(shopcart.items, shopcarts[1].items)

    def test_find_by_name(self):
        """ Test Finds a Shopcart by it's name """
        Shopcart(user_id = 0,name="Alice", items = []).create()
        shopcart = Shopcart.find_by_name("Alice")
        self.assertEqual(shopcart.user_id, 0)
        self.assertEqual(shopcart.name, "Alice")
        self.assertEqual(shopcart.items, [])
    
    def test_find_or_404_found(self):
        """Test Find or return 404 found"""
        shopcart1 = Shopcart(user_id = 0,name="Alice", items = [])
        shopcart2 = Shopcart(user_id = 1, name="Bob", items = [])
        shopcart3 = Shopcart(user_id = 2, name = "Kevin", items = [])
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        shopcart = Shopcart.find_or_404(shopcarts[1].user_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, shopcarts[1].user_id)
        self.assertEqual(shopcart.name, shopcarts[1].name)
        self.assertEqual(shopcart.items, shopcarts[1].items)

    def test_find_or_404_not_found(self):
        """Test Find or return 404 found"""
        self.assertRaises(NotFound, Shopcart.find_or_404, 0)
    
