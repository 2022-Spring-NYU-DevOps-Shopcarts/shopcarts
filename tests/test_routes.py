"""
TestShopcart API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db

######################################################################
#  T E S T   C A S E S
######################################################################
class ShopcartsServerTest(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.testing = True

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_shopcarts_get(self):
        """ Test GET on /shopcarts"""
        resp = self.app.get("/shopcarts")
        data = resp.get_json()
        self.assertEqual(data, "GET call received at /shopcarts.")

    def test_shopcarts_post(self):
        """ Test POST on /shopcarts"""
        resp = self.app.post("/shopcarts")
        data = resp.get_json()
        self.assertEqual(data, "POST call received at /shopcarts.")

    def test_shopcarts_put(self):
        """ Test PUT on /shopcarts"""
        resp = self.app.put("/shopcarts")
        data = resp.get_json()
        self.assertEqual(data, "PUT call received at /shopcarts.")

    def test_shopcarts_delete(self):
        """ Test DELETE on /shopcarts"""
        resp = self.app.delete("/shopcarts")
        data = resp.get_json()
        self.assertEqual(data, "DELETE call received at /shopcarts.")
        