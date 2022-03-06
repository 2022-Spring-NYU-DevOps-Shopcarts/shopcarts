"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os

from sqlalchemy import null, true
from service.models import Shopcart, Item, DataValidationError, db
from service import app

######################################################################
#  Shopcart   M O D E L   T E S T   C A S E S
######################################################################
class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

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
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_repr(self):
        """ Test __repr__ """
        test_obj = Shopcart()
        res = test_obj.__repr__()
        self.assertEqual(res, "<Shopcart None id=[None]>")

    def test_create_shopcart(self):
        shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        self.assertEqual(shopcart.user_id, 0)
        self.assertEqual(shopcart.name, "Alice")
        self.assertEqual(shopcart.items, [])

    def test_create_without_item(self):
        """ Test create a Shopcart with no item, add it to the database"""
        # shopcarts = Shopcart.all()
        # self.assertEqual(shopcarts, [])
        # shopcart = Shopcart(user_id = 0,name="Alice", items = [])
        # shopcart.create()
        # shopcarts = Shopcart.all()
        # self.assertEqual(len(shopcarts), 1)

        


    
        
        
