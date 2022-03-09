"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Shopcart, DataValidationError
from werkzeug.exceptions import NotFound

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
    app.logger.info("Request to create a pet")
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
# RETRIEVE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", shopcart_id)
    shopcart = Shopcart.find_shopcart(shopcart_id) #This is the list of shopcarts which user_id == shopcart_id
    if not shopcart:
        raise NotFound("Shopcart with id '{}' was not found.".format(shopcart_id))
    app.logger.info("Returning shopcart: %s", shopcart_id)
    return make_response(jsonify([sc.serialize() for sc in shopcart if sc.item_id != -1]), status.HTTP_200_OK) #As 1 user is attached to 1 user_id

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