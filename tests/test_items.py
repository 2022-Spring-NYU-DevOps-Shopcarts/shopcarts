"""
Test cases for Item in Shopcart

"""
from csv import unregister_dialect
import logging
import unittest
import os

from sqlalchemy import null, true
from service.models import Item, DataValidationError, db

######################################################################
#  Item   T E S T   C A S E S
######################################################################

class TestItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        # db.drop_all() # drop all previous test records
        pass

    def tearDown(self):
        """ This runs after each test """
        pass


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_repr(self):
        item = Item(item_name="rings", quantity="2", price="1000")
        self.assertEqual(item.__repr__(), "<Item rings, quantity=[2], price=[1000]>")

    def test_serialize(self):
        item = Item(item_name="rings", quantity=2, price=1000)
        data = item.serialize()
        self.assertIn("item_name", data)
        self.assertEqual(data["item_name"], "rings")
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], 2)
        self.assertIn("price", data)
        self.assertEqual(data["price"], 1000)

    def test_deserialize(self):
        data = {"item_name" : "rings", "quantity" : 2, "price" : 1000, "user_id" : 0}
        item = Item()
        item.deserialize(data)
        self.assertEqual(item.item_name, "rings")
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, 1000)
    
    def test_deserialize_key_missing(self):
        data = {"item_name" : "rings", "quantity" : 2}
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)
    
    def test_deserialize_bad_data(self):
        data = "I am meant to be a dictionary, but I am not"
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)