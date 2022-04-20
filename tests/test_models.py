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
from tests.factories import ItemFactory

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
        item_in_shopcart = ItemFactory()
        res = item_in_shopcart.__repr__()
        logging.debug(item_in_shopcart)
        self.assertEqual(res, "<Product %s in Shopcart for user %s>"
         % (item_in_shopcart.item_id, item_in_shopcart.user_id))


    def test_create_a_shopcart(self):
        """Create a shopcart and assert that it exists"""
        shopcart = Shopcart(user_id = 0, item_id = 1, item_name = "ring", quantity = 2, price = 10.5)
        logging.debug(shopcart)
        self.assertTrue(shopcart is not None)
        self.assertEqual(shopcart.user_id, 0)
        self.assertEqual(shopcart.item_id, 1)
        self.assertEqual(shopcart.item_name, "ring")
        self.assertEqual(shopcart.quantity, 2)
        self.assertEqual(shopcart.price, 10.5)


    def test_add_a_shopcart(self):
        """ Test create a Shopcart, add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ItemFactory()
        logging.debug(shopcart)
        shopcart.create()
        shopcarts = Shopcart.all_shopcart()
        self.assertEqual(len(shopcarts), 1)


    def test_add_a_item(self):
        """ Update a Shopcart, add a new item"""
        shopcart = ItemFactory()
        shopcart.create()
        logging.debug(shopcart)
        item_in_shopcart = Shopcart(user_id = shopcart.user_id, item_id = shopcart.item_id+1, item_name = "rings", quantity = 2, price = 1000)
        self.assertEqual(item_in_shopcart.item_name, "rings")
        self.assertEqual(item_in_shopcart.quantity, 2)
        self.assertEqual(item_in_shopcart.price, 1000)
        item_in_shopcart.create()
        logging.debug(item_in_shopcart)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 2)


    def test_update_a_item(self):
        """ Update a Shopcart, change item quantity"""
        item_in_shopcart = ItemFactory()
        item_in_shopcart.create()
        logging.debug(item_in_shopcart)
        # Change it and save it
        item_in_shopcart.quantity += 3
        item_in_shopcart.save()
        # Fetch it back and make sure the user id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        item = Shopcart.find_item(item_in_shopcart.user_id, item_in_shopcart.item_id)
        self.assertEqual(item.item_name, item_in_shopcart.item_name)
        self.assertEqual(item.quantity, item_in_shopcart.quantity)


    def test_delete_a_shopcart(self):
        """ Delete a Shopcart"""
        shopcart = ItemFactory()
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        logging.debug(shopcart)
        # delete the shopcart and make sure it isn't in the database
        shopcart.delete()
        self.assertEqual(len(Shopcart.all()), 0)


    def test_serialize_a_shopcart(self):
        """Test serialization of a Shopcart"""
        item_in_shopcart = ItemFactory()
        data = item_in_shopcart.serialize()
        logging.debug(item_in_shopcart)
        self.assertIn("user_id", data)
        self.assertEqual(data["user_id"], item_in_shopcart.user_id)
        self.assertIn("item_id", data)
        self.assertEqual(data["item_id"], item_in_shopcart.item_id)
        self.assertIn("item_name", data)
        self.assertEqual(data["item_name"], item_in_shopcart.item_name)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], item_in_shopcart.quantity)
        self.assertIn("price", data)
        self.assertEqual(data["price"], item_in_shopcart.price)


    def test_deserialize_a_shopcart(self):
        """Test deserialization of a Shopcart"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : 20.5}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        logging.debug(shopcart)
        self.assertEqual(shopcart.item_name, "bottle")
        self.assertEqual(shopcart.quantity, 2)
        self.assertEqual(shopcart.price, 20.5)


    def test_deserialize_with_hold(self):
        """Test deserialization of a Shopcart with hold info"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : 20.5, "hold" : True}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        logging.debug(shopcart)
        self.assertEqual(shopcart.item_name, "bottle")
        self.assertEqual(shopcart.quantity, 2)
        self.assertEqual(shopcart.price, 20.5)
        self.assertEqual(shopcart.hold, True)


    def test_deserialize_with_bad_hold(self):
        """Test deserialization of a Shopcart with hold info"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : 20.5, "hold" : 1}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_missing_data(self):
        """Test deserialization of a Shopcart with missing data"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_bad_userid(self):
        """Test deserialization of a Shopcart with non-int user_id"""
        data = {"user_id" : 1.5, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : 20.5}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_bad_quantity(self):
        """Test deserialization of a Shopcart with non-int quantity"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2.5, "price" : 20.5}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_bad_price(self):
        """Test deserialization of a Shopcart with non-number price"""
        data = {"user_id" : 1, "item_id" : 2, "item_name" : "bottle", "quantity" : 2, "price" : "true"}
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)


    def test_deserialize_bad_data(self):
        """Test deserialization of a Shopcart with bad data"""
        data = "This is not a dictionary"
        shopcart = Shopcart()
        logging.debug(shopcart)
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    
    def test_find_shopcart(self):
        """ Test Finds a Shopcart by user id """
        shopcart1 = ItemFactory(item_id = 0)
        shopcart2 = ItemFactory(user_id = shopcart1.user_id, item_id = 1)
        shopcart3 = ItemFactory(user_id = shopcart1.user_id, item_id = 2)
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        # make sure they got saved
        self.assertEqual(len(Shopcart.all()), 3)
        retrieved_shopcarts = Shopcart.find_shopcart(shopcart1.user_id)
        # check each shopcart info got matched
        for i in range(len(retrieved_shopcarts)):
            self.assertIsNot(retrieved_shopcarts[i], None)
            self.assertEqual(retrieved_shopcarts[i].user_id, shopcarts[i].user_id)
            self.assertEqual(retrieved_shopcarts[i].item_id, shopcarts[i].item_id)
            self.assertEqual(retrieved_shopcarts[i].item_name, shopcarts[i].item_name)
            self.assertEqual(retrieved_shopcarts[i].quantity, shopcarts[i].quantity)
            self.assertEqual(retrieved_shopcarts[i].price, shopcarts[i].price)

    
    def test_find_shopcart_or_404_found(self):
        """ Test Found a Shopcart by user id """
        shopcart_base = ItemFactory()
        shopcart_base.create()
        self.assertEqual(len(Shopcart.all()), 1)
        retrieved_shopcart = Shopcart.find_shopcart_or_404(shopcart_base.user_id)
        self.assertIsNotNone(retrieved_shopcart)
        self.assertEqual(retrieved_shopcart.user_id, shopcart_base.user_id)
        self.assertEqual(retrieved_shopcart.item_id, shopcart_base.item_id)


    def test_find_shopcart_or_404_not_found(self):
        """ Test Do not find a Shopcart by user id """
        self.assertRaises(NotFound, Shopcart.find_shopcart_or_404, 0)


    def test_find_item(self):
        """ Test Finds a Shopcart-Item by user id, item id """
        shopcart1 = ItemFactory(item_id = 0)
        shopcart2 = ItemFactory(user_id = shopcart1.user_id, item_id = 1)
        shopcart3 = ItemFactory(user_id = shopcart1.user_id, item_id = 2)
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        # make sure they got saved
        self.assertEqual(len(Shopcart.all()), 3)
        # find the second shopcart in the list
        shopcart = Shopcart.find_item(shopcarts[1].user_id, shopcarts[1].item_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, shopcarts[1].user_id)
        self.assertEqual(shopcart.item_id, shopcarts[1].item_id)
        self.assertEqual(shopcart.item_name, shopcarts[1].item_name)
        self.assertEqual(shopcart.quantity, shopcarts[1].quantity)
        self.assertEqual(shopcart.price, shopcarts[1].price)

    
    def test_find_item_or_404_found(self):
        """ Test Found a Shopcart-Item by user id, item id """
        shopcart1 = ItemFactory(item_id = 0)
        shopcart2 = ItemFactory(user_id = shopcart1.user_id, item_id = 1)
        shopcart3 = ItemFactory(user_id = shopcart1.user_id, item_id = 2)
        shopcarts = [shopcart1, shopcart2, shopcart3]
        for shopcart in shopcarts:
            shopcart.create()
        # make sure they got saved
        self.assertEqual(len(Shopcart.all()), 3)
        # find the second shopcart in the list
        shopcart = Shopcart.find_item_or_404(shopcarts[1].user_id, shopcarts[1].item_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, shopcarts[1].user_id)
        self.assertEqual(shopcart.item_id, shopcarts[1].item_id)
        self.assertEqual(shopcart.item_name, shopcarts[1].item_name)
        self.assertEqual(shopcart.quantity, shopcarts[1].quantity)
        self.assertEqual(shopcart.price, shopcarts[1].price)


    def test_find_item_or_404_not_found(self):
        """Test 404 for item"""
        self.assertRaises(NotFound, Shopcart.find_item_or_404, 0, -1)
    
