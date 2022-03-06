"""
My Service

TODO: Describe what your service does here
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

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request root URL response...")
    # TODO: fill in below with complete API instructions when done
    return (
        jsonify(
            name="Shopcarts Microservice",
            version="1.0.0",
            paths=url_for("list_shopcarts", _external=True),
        ),
        status.HTTP_200_OK,
    )


############################################################
#                 R E S T   A P I
############################################################

#-----------------------------------------------------------
# Service skeleton demonstrating GET, POST, PUT, DELETE
# Get shopcarts
#-----------------------------------------------------------
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """TODO: currently is dummy code
    Lists all of the shopcarts in the database

    Returns:
        list: an array of shopcart names
    """
    #app.logger.info("Request to list all shopcarts...")

    # Get the database key names as a list
    #names = counter.keys("*")
    #return jsonify(names)
    return jsonify("GET call received at /shopcarts.")


#-----------------------------------------------------------
# Create shopcarts
#-----------------------------------------------------------
@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """ TODO: currently is dummy code
    Creates a new counter and stores it in the database

    Args:
        name (str): the name of the counter to create

    Returns:
        dict: the counter and it's value
    """
    #app.logger.info(f"Request to Create counter {name}...")

    # See if the counter already exists and send an error if it does
    #count = counter.get(name)
    #if count is not None:
    #    abort(HTTP_409_CONFLICT, f"Counter {name} already exists")

    # Create the new counter and set it to zero
    #counter.set(name, 0)

    # Set the location header and return the new counter
    #location_url = url_for("read_counters", name=name, _external=True)
    return (jsonify("POST call received at /shopcarts."))


#-----------------------------------------------------------
# Read counters
#-----------------------------------------------------------
@app.route("/shopcarts/<name>", methods=["GET"])
def read_shopcarts():
    """TODO: currently is dummy code
    Reads a counter from the database

    Args:
        name (str): the name of the counter to read

    Returns:
        dict: the counter and it's value
    """
    #app.logger.info(f"Request to Read counter {name}...")

    # Get the current counter
    #count = counter.get(name)

    # Send an error if it does not exist
    #if count is None:
    #    abort(HTTP_404_NOT_FOUND, f"Counter {name} does not exist")

    # Return the counter
    # return jsonify(name=name, counter=int(count))
    pass


#-----------------------------------------------------------
# Update shopcarts
#-----------------------------------------------------------
@app.route("/shopcarts", methods=["PUT"])
def update_shopcarts():
    """TODO: currently is dummy code
    Updates a counter in the database

    Args:
        name (str): the name of the counter to update

    Returns:
        dict: the counter and it's value
    """
    #app.logger.info(f"Request to Update counter {name}...")

    # Get the current counter
    #count = counter.get(name)

    # Send an error if it does not exist
    #if count is None:
    #    abort(HTTP_404_NOT_FOUND, f"Counter {name} does not exist")

    # Increment the counter and return the new value
    #count = counter.incr(name)
    return jsonify("PUT call received at /shopcarts.")


#-----------------------------------------------------------
# Delete shopcarts
#-----------------------------------------------------------
@app.route("/shopcarts", methods=["DELETE"])
def delete_shopcarts():
    """TODO: currently is dummy code
    Delete a counter from the database

    Args:
        name (str): the name of the counter to delete

    Returns:
        str: always returns an empty string
    """
    #app.logger.info(f"Request to Delete counter {name}...")

    # Get the current counter
    #count = counter.get(name)

    # If it exists delete it, if not do nothing
    #    counter.delete(name)
    #if count is not None:

    # Delete always returns 204
    return jsonify("DELETE call received at /shopcarts.")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Shopcart.init_db(app)
