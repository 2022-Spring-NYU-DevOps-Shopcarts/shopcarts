"""
My Service

Describe what your service does here
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
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
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
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("get_shopcarts", shopcart_id=shopcart.user_id, _external=True)

    app.logger.info("Shopcart with ID [%s] created.", shopcart.user_id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# RETRIEVE A PET
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on it's id
    """

######################################################################
# UPDATE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods = ["PUT"])
def update_shopcart(shopcart_id):
    """
    Updates shopcart with the relevant shopcart_id to quantity

    Args:
        shopcart_id (int): The shopcart to be updated
        body of API call (JSON): [item_id, quantity]

    Returns:
        status code: 200 if successful, 404 if cart not found,
            406 if quantity is not a non-negative integer.
        message (JSON): new state of shopcart or empty if cart not found
    """
    check_content_type("application/json")
    item_quantity = request.get_json()
    item_id = item_quantity["item_id"]
    try:
        assert isinstance(item_quantity["quantity"], int)
        assert item_quantity["quantity"] >= 0
    except (TypeError, AssertionError):
        app.logger.error("Quantity %s must be a non-negative integer.", item_quantity["quantity"])
        return make_response(jsonify(""), status.HTTP_406_NOT_ACCEPTABLE)
    quantity = int(item_quantity["quantity"])
    app.logger.info(
        "Request to modify shopcart id %s: change quantity of \
        item id %s to %s...", shopcart_id, item_id, quantity
    )    
    try:
        shopcart = Shopcart.find_shopcart_or_404(shopcart_id)
    except NotFound:
        app.logger.error("Shopcart %s not found.", item_id)
        return make_response(jsonify(""), status.HTTP_404_NOT_FOUND)

    user_id = shopcart_id
    try:
        item = Shopcart.find_item_or_404(user_id, item_id)
        if quantity == 0:
            app.logger.info(
            "Deleting item %s from cart %s...",
            item_id, user_id
            )
            item.delete()
            return make_response(
                jsonify(""), status.HTTP_200_OK
            )
        else:
            app.logger.info(
                "Updating item %s to quantity %s in cart %s...",
                item_id, quantity, shopcart_id
                )
            item.quantity = quantity
            item.create()
            return make_response(
                jsonify(item.serialize()), status.HTTP_200_OK)
    except NotFound:
        if quantity == 0:
            app.logger.info("No changes to cart %s", user_id)
            return make_response(
                jsonify(""), status.HTTP_200_OK
                )
        else:
            app.logger.info(
                "Item %s not found in cart %s, creating...",
                item_id, user_id
                )
            item =  Shopcart(
                user_id = user_id,
                item_id = item_id,
                quantity = quantity
                )
            item.create()
            return make_response(
                jsonify(item.serialize()), 
                status.HTTP_200_OK
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
   
    