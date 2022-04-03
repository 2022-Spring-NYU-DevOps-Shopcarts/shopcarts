"""
name: Shopcarts Service
version: 1.0
resource URLs: /shopcarts/<user-id>

Allows different users to store items in their shopcarts.

Usage: 
    POST   on /shopcarts: creates new shopcart based on body data
    GET    on /shopcarts: returns list of all shopcarts
    PUT    on /shopcarts/<user-id>: add/delete items in <user-id> shopcart
    GET    on /shopcarts/<user-id>: returns items in <user-id> shopcart
    DELETE on /shopcarts/<user-id>: deletes <user-id> shopcart

"""

from multiprocessing.sharedctypes import Value
import os
import sys
import logging
from typing import Type
from werkzeug.exceptions import NotFound
from flask import Flask, jsonify, request, url_for, make_response, abort
from service.error_handlers import not_found
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Shopcart, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    info = {"name": "Shopcarts Service", "version": "1.0", "resource URL": "/shopcarts"} 
    app.logger.info("Root URL response")
    return (
        make_response(jsonify(info),status.HTTP_200_OK)
    )

######################################################################
# ADD A NEW SHOPCART
######################################################################
@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a Shopcart
    This endpoint will create a Shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    req = request.get_json()
    if not "user_id" in req.keys() or not isinstance(req["user_id"], int):
        abort(status.HTTP_400_BAD_REQUEST, f"Invalid user id.")
    if Shopcart.find_shopcart(req["user_id"]):
        user_id = req["user_id"]
        abort(
            status.HTTP_400_BAD_REQUEST, 
            f"User with id '{user_id}' already has a non-empty shopcart.",
        )
    
    shopcarts = []
    shopcarts_deserialize = []
    if "item_id" in req.keys():
        shopcarts.append(req)
    elif "items" in req.keys():
        shopcarts = req["items"]
    for s in shopcarts:
        s["user_id"] = req["user_id"]
        shopcart = Shopcart()
        shopcart.deserialize(s)
        shopcart.create()
        shopcarts_deserialize.append(shopcart)
    location_url = url_for("get_shopcarts", shopcart_id=req["user_id"], _external=True)
    app.logger.info("Shopcart with ID [%s] created.", req["user_id"])
    results = [shopcart.serialize() for shopcart in shopcarts_deserialize]
    return make_response(
        jsonify(results), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL SHOPCARTS
######################################################################
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """Returns all of the Shopcarts"""
    # app.logger.info("Request for shopcart list")
    # shopcarts = Shopcart.all_shopcart()
    # results = [shopcart.serialize() for shopcart in shopcarts]
    # app.logger.info("Returning %d shopcarts", len(results))
    # return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on its id
    """
    app.logger.info("Request for shopcart with id: %s", shopcart_id)
    #This is the list of shopcarts which user_id == shopcart_id
    shopcart = Shopcart.find_shopcart(shopcart_id) 
    if not shopcart:
        raise NotFound(
            "Shopcart with id '{}' was not found.".format(shopcart_id)
            )
    app.logger.info("Returning shopcart: %s", shopcart_id)
    #As 1 user is attached to 1 user_id
    return make_response(jsonify(
        [sc.serialize() for sc in shopcart]),
        status.HTTP_200_OK
        ) 

######################################################################
# DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["DELETE"])
def delete_shopcarts(shopcart_id):
    """
    Delete a single Shopcart
    This endpoint will return a Shopcart based on its id
    """
    app.logger.info("Request to delete shopcart with id: %s", shopcart_id)
    shopcart = Shopcart.find_shopcart(shopcart_id) 
    if shopcart:
        for item in shopcart:
            item.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE A SHOPCART (#TODO: TO BE FIXED)
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods = ["PUT"])
def update_shopcarts(shopcart_id):
    """
    Updates shopcart with the relevant shopcart_id to quantity

    Args:
        shopcart_id (int): The shopcart to be updated
        body of API call (JSON): 
            item_id (int)
            quantity (int) 
            item_name 
            price (float)

    Returns:
        status code: 200 if successful, 404 if cart not found,
            406 if data type errors.
        message (JSON): new state of shopcart or empty if cart not found
    """
    # check_content_type("application/json")
    # item_quantity = request.get_json()
    # item_id = item_quantity["item_id"]
    # try:
    #     assert isinstance(item_quantity["quantity"], int)
    #     assert item_quantity["quantity"] >= 0
    # except (TypeError, AssertionError):
    #     app.logger.error(
    #         "Quantity %s must be a non-negative integer.",
    #         item_quantity["quantity"]
    #         )
    #     return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    # quantity = int(item_quantity["quantity"])
    # app.logger.info(
    #     "Request to modify shopcart id %s: change quantity of \
    #     item id %s to %s...", shopcart_id, item_id, quantity
    # )    
    # # Make sure this shopcart exists
    # Shopcart.find_shopcart_or_404(shopcart_id)
    # user_id = shopcart_id
    # try:
    #     item = Shopcart.find_item_or_404(user_id, item_id)
    #     if quantity == 0:
    #         app.logger.info(
    #         "Deleting item %s from cart %s...",
    #         item_id, user_id
    #         )
    #         item.delete()
    #         return make_response(
    #             jsonify(""), status.HTTP_200_OK
    #         )
    #     else:
    #         app.logger.info(
    #             "Updating item %s to quantity %s in cart %s...",
    #             item_id, quantity, shopcart_id
    #             )
    #         item.quantity = quantity
    #         item.create()
    #         return make_response(
    #             jsonify(item.serialize()), status.HTTP_200_OK
    #             )
    # except NotFound:
    #     if quantity == 0:
    #         app.logger.info("No changes to cart %s", user_id)
    #         return make_response(
    #             jsonify(""), status.HTTP_200_OK
    #             )
    #     else:
    #         app.logger.info(
    #             "Item %s not found in cart %s, creating...",
    #             item_id, user_id
    #             )
    #         item_name = item_quantity["item_name"]
    #         try:
    #             assert isinstance(item_quantity["price"], float)
    #             assert item_quantity["price"] >= 0
    #         except (TypeError, AssertionError):
    #             app.logger.error(
    #                 "Price %s must be a non-negative number.", item_quantity["price"]
    #                 )
    #             return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    #         price = float(item_quantity["price"])
    #         item =  Shopcart(
    #             user_id = user_id,
    #             item_id = item_id,
    #             item_name = item_name,
    #             price = price,
    #             quantity = quantity
    #             )
    #         item.create()
    #         return make_response(
    #             jsonify(item.serialize()), 
    #             status.HTTP_200_OK
    #         )


######################################################################
# CREATE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods = ["POST"])
def create_items(shopcart_id):
    """
    #TODO: docstring
    Updates shopcart with the relevant shopcart_id to quantity

    Args:
        shopcart_id (int): The shopcart to be updated
        body of API call (JSON): 
            item_id (int)
            quantity (int) 
            item_name 
            price (float)

    Returns:
        status code: 200 if successful, 404 if cart not found,
            406 if data type errors.
        message (JSON): new state of shopcart or empty if cart not found
    """
    check_content_type("application/json")
    item = request.get_json()
    app.logger.info("Received item %s...", item)
    try:
        assert isinstance(item["quantity"], int)
        assert item["quantity"] > 0      
    except (TypeError, AssertionError):
        app.logger.error(
            "Quantity %s must be a positive integer.",
            item["quantity"]
            )
        return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    try:
        assert isinstance(item["item_id"], int)
        assert item["item_id"] >= 0
    except (TypeError, AssertionError):
        app.logger.error(
            "Item_id %s must be a non-negative integer.",
            item["item_id"]
            )
        return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    try:
        assert isinstance(item["item_name"], Str)
    except AssertionError:
        app.logger.error(
            "Item_name %s must be a string.",
            item["item_name"]
            )
        return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    try:
        assert isinstance(item["price"], int) or isinstance(item["price"], float)
        assert item["quantity"] >= 0      
    except (TypeError, AssertionError):
        app.logger.error(
            "Price %s must be a non-negative integer.",
            item["price"]
            )
        return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)

    #TODO: assert item_id not already in this cart after GET implemented
    item =  Shopcart(
        user_id = shopcart_id,
        item_id = int(item["item_id"]),
        item_name = item["item_name"],
        price = float(item["price"]),
        quantity = int(item["quantity"])
        )

    app.logger.info(
        "Request to create item %s with user_id %s,  item_name %s, price %s, \
            quantity %s...", item.item_id, item.user_id, item.item_name, item.price, item.quantity
    )    
    item.create()
    return make_response(
        jsonify(item.serialize()), status.HTTP_200_OK
        )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
   
    