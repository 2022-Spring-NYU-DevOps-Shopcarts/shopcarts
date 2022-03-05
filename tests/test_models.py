"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os

from sqlalchemy import null, true
from service.models import YourResourceModel, DataValidationError, db

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

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
        test_obj = YourResourceModel()
        res = test_obj.__repr__()
        self.assertEqual(res, "<YourResourceModel None id=[None]>")

    def test_create(self):
        """ Test create """
        test_obj = YourResourceModel()
        table_data = db.session.query(YourResourceModel).all()
        test_obj.name = 'ZhengruiXia'

        test_obj.create()

        p_table_data = db.session.query(YourResourceModel).all()
        test_obj.delete()

        self.assertTrue(len(table_data) == len(p_table_data) - 1)


    def test_delete(self):
        """ Test delete """
        test_obj = YourResourceModel()
        test_obj.name = "ZhengruiXia"
        test_obj.create()
        table_len = len(db.session.query(YourResourceModel).all())
        test_obj.delete()
        p_table_len = len(db.session.query(YourResourceModel).all())
        
        self.assertTrue(table_len == p_table_len + 1)

    def test_save(self):
        """ Test save """
        test_obj = YourResourceModel()
        test_obj.name = "ZhengruiXia"
        db.session.add(test_obj)
        test_obj.save()
        test_obj.delete()
        self.assertTrue(True)

    def test_serialize(self):
        """ Test serialize """
        test_obj = YourResourceModel()
        test_obj.name = "ZhengruiXia"
        test_obj.id = 1
        res = test_obj.serialize()
        self.assertEqual(res, {"id": 1, "name": "ZhengruiXia"})

    def test_deserialize(self):
        """ Test deserialize """
        test_obj = YourResourceModel()
        test_obj.deserialize({"id": 1, "name": "ZhengruiXia"})
        self.assertEqual(test_obj.name, "ZhengruiXia")
        try:
            test_obj.deserialize({"id": 1, "nAmel": "ZhengruiXia01"})
        except DataValidationError:
            self.assertTrue(True)
        try:
            test_obj.deserialize({"id": 1, "name": 33})
        except DataValidationError:
            self.assertTrue(True)

    def test_class_all(self):
        """ Test class.all """
        test_obj = YourResourceModel()
        test_obj.name = "ZhengruiXia"
        table_data = YourResourceModel.all()
        test_obj.create()
        p_table_data = YourResourceModel.all()
        test_obj.delete()
        self.assertEqual(len(table_data), len(p_table_data) - 1)

    def test_class_find(self):
        """ Test class.find and class.find_by_name """
        test_obj = YourResourceModel()
        test_obj.name = "ZhengruiXia"
        test_obj.create()
        print(YourResourceModel.all())
        res = YourResourceModel.find(121)
        # TODO: Test find_or_404 (How to catch 404 not found error?)
        res = YourResourceModel.find_or_404(121)
        res = YourResourceModel.find_by_name("ZhengruiXia")
        test_obj.delete()
        print(res)
        self.assertTrue(True)
        
        
        
        

        

