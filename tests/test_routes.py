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
from flask import jsonify
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import ShopcartFactory, ItemFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/shopcarts"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
    
    def _create_shopcarts(self, count):
        """Factory method to create shopcarts in bulk"""
        shopcarts = []
        for i in range(count):
            test_shopcart = ShopcartFactory()
            resp = self.app.post(
                BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart"
            )
            shopcarts.append(test_shopcart)
        return shopcarts

    def _create_items(self, count):
        """Factory method to create items in shopcart in bulk"""
        shopcart = ShopcartFactory()
        resp = self.app.post(
                BASE_URL, json=shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        shopcarts = []
        for i in range(count):
            test_item = ItemFactory(user_id = shopcart.user_id, item_id = i)
            resp = self.app.put(
                "{0}/{1}".format(BASE_URL, shopcart.user_id),
                json=test_item.serialize(),
                content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_200_OK, "Could not create test items in shopcart"
            )
            shopcarts.append(test_item)
        return shopcarts



    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_shopcart_list(self):
        """Get a list of Shopcart"""
        self._create_shopcarts(2)
        self._create_items(3) #one more shopcart with items
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 3)

    def test_get_shopcart(self):
        """Get a shopcart"""
        # get the items of a shopcart
        test_shopcart = self._create_items(3)
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_shopcart[0].user_id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data),len(test_shopcart))
        for i in range(len(test_shopcart)):
            self.assertEqual(data[i]['item_id'], test_shopcart[i].item_id)
            self.assertEqual(data[i]['item_name'], test_shopcart[i].item_name)
            self.assertEqual(data[i]['quantity'], test_shopcart[i].quantity)
            self.assertEqual(data[i]['price'], test_shopcart[i].price)

    def test_get_shopcart_not_found(self):
        """Get a Shopcart thats not found"""
        resp = self.app.get("/shopcarts/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_method_not_supported(self):
        """Test Method Not Supported"""
        resp = self.app.put(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_shopcart(self):
        """Create a new Shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["user_id"], test_shopcart.user_id, "User IDs do not match")
        self.assertEqual(new_shopcart["item_id"], test_shopcart.item_id, "item IDs do not match")
        # Check that the location header was correct
        test_item = ItemFactory(user_id = test_shopcart.user_id)
        resp = self.app.put(location, json=test_item.serialize(), content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart[0]["user_id"], test_shopcart.user_id, "User IDs do not match")

    def test_create_shopcart_no_data(self):
        """Create a Shopcart with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart_no_content_type(self):
        """Create a Shopcart with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_shopcart_bad_id(self):
        """Create a Shopcart with bad user ID or bad item ID (not -1)"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        # change user ID to a string
        test_shopcart.user_id = "true"
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        test_shopcart = ItemFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_shopcart(self):
        """Update a shopcart with a new item"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Check the data is correct
        new_item = resp.get_json()
        self.assertEqual(new_item["user_id"], test_shopcart.user_id, "User IDs do not match")
        self.assertEqual(new_item["item_id"], item_in_shopcart.item_id, "Item IDs do not match")
        self.assertEqual(new_item["quantity"], item_in_shopcart.quantity, "Quantities do not match")

    def test_update_shopcart_quantity(self):
        """Update a shopcart with correct quantity"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.quantity = 1
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart.quantity = 3
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_item = resp.get_json()
        self.assertEqual(new_item["user_id"], test_shopcart.user_id, "User IDs do not match")
        self.assertEqual(new_item["item_id"], item_in_shopcart.item_id, "Item IDs do not match")
        self.assertEqual(new_item["quantity"], item_in_shopcart.quantity, "Quantities do not match")

    def test_update_shopcart_bad_quantity(self):
        """Attempts to update a shopcart with bad quantity"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.quantity = 1.5
        logging.debug("New quantity is %s...", item_in_shopcart.quantity)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_negative_quantity(self):
        """Attempts to update a shopcart with negative quantity"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.quantity = -1
        logging.debug("New quantity is %s...", item_in_shopcart.quantity)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_zero_quantity(self):
        """Update an item in shopcart to 0 quantity"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id, quantity = 3)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart.quantity = 0
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_zero_quantity_no_change(self):
        """Update a non-existent item in shopcart to 0 quantity (nothing happens)."""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id, quantity = 0)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart.quantity = 0
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_bad_price(self):
        """Attempts to update a shopcart with bad price"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.price = "k"
        logging.debug("New price is %s...", item_in_shopcart.price)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_negative_price(self):
        """Attempts to update a shopcart with negative price"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.price = -1.5
        logging.debug("New price is %s...", item_in_shopcart.price)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(resp.get_json(), "")

    def test_update_shopcart_not_found(self):
        """Attempts update on a non-existent shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        url = BASE_URL + "/" + str(test_shopcart.user_id)
        resp = self.app.put(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_empty_shopcart(self):
        """Test delete an existing shopcart with no other items added"""
        shopcart = ShopcartFactory()
        shopcart.create()
        resp = self.app.delete(
            "/shopcarts/{}".format(shopcart.user_id),
            content_type = "shopcarts/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_shopcart_with_items(self):
        shopcart = self._create_items(3)
        resp = self.app.delete(
            "/shopcarts/{}".format(shopcart[0].user_id),
            content_type = "shopcarts/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_shopcart_not_found(self):
        """Delete a Shopcart that's not found"""
        resp = self.app.delete("/shopcarts/0")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_item(self):
        """Creates an item"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        logging.debug(item_in_shopcart)
        logging.debug(item_in_shopcart.item_id)
        logging.debug(item_in_shopcart.item_name)
        logging.debug(item_in_shopcart.user_id)
        logging.debug(item_in_shopcart.price)
        logging.debug(item_in_shopcart.quantity)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        logging.debug(url)
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        logging.debug(resp)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_item = resp.get_json()
        self.assertEqual(new_item["user_id"], test_shopcart.user_id, "User IDs do not match")
        self.assertEqual(new_item["item_id"], item_in_shopcart.item_id, "Item IDs do not match")
        self.assertEqual(new_item["quantity"], item_in_shopcart.quantity, "Quantities do not match")
        self.assertAlmostEqual(new_item["price"], item_in_shopcart.price, "Prices do not match")
    
    def test_create_item_bad_name(self):
        """Attempts to create an item with non-string name"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.item_name = 9
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_create_item_bad_id(self):
        """Attempts to create an item with a non-positive int id"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.item_id = "foo"
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_item_bad_quantity(self):
        """Attempts to create an item with a non-positive int id"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.quantity = 0
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_item_negative_price(self):
        """Attempts to create an item with a negative float """
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.price = -0.5
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        
    def test_create_item_bad_price(self):
        """Attempts to create an item with a string as price """
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id)
        item_in_shopcart.price = "bar"
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    """ # TODO: Uncomment below after GET item implemented
        # and duplicate item_id checking implemented
    def test_create_item_duplicate_id(self):       
        # TODO: docstring goes here
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id, item_id = 1)
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        item_in_shopcart = ItemFactory(user_id = test_shopcart.user_id, item_id = 1)
        logging.debug(item_in_shopcart)
        url = BASE_URL + "/" + str(test_shopcart.user_id) + "/items"
        resp = self.app.post(
            url, json=item_in_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
    """
    