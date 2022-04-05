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
from werkzeug.exceptions import NotFound
from flask import jsonify, request, url_for, make_response, abort
from service.models import Shopcart
from .utils import status  # HTTP Status Codes

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Root URL response")
    return app.send_static_file("index.html")

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


# Zhengrui Xia: Changed to Shopcart.all from Shopcart.all_shopcart since if a 
# shopcart is empty, it won't exist in our database
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """Returns all of the Shopcarts"""
    app.logger.info("Request for shopcart list")
    shopcarts = Shopcart.all_shopcart()
    results = [dict(shopcart) for shopcart in shopcarts]
    app.logger.info("Returning %d shopcarts", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

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
        return make_response(jsonify([]), status.HTTP_200_OK) 

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
    Create new item in shopcart {shopcart_id}.

    Args:
        shopcart_id (int): The shopcart to be updated
        body of API call (JSON): 
            item_id (int)
            quantity (int) 
            item_name (string)
            price (float/int)

    Returns:
        status code: 201 if successful, 409 if already exists,
            400 if data type errors.
        message (JSON): new item if successful, empty if not.
    """
    check_content_type("application/json")
    item = request.get_json()
    app.logger.info("Received item %s...", item)
    try:
        assert isinstance(item["quantity"], int)
        assert item["quantity"] > 0      
    except (TypeError, AssertionError, KeyError):
        app.logger.error("Quantity must be a positive integer.")
        abort(status.HTTP_400_BAD_REQUEST, "Quantity must be a positive integer.")
    try:
        assert isinstance(item["item_id"], int)
        assert item["item_id"] >= 0
    except (TypeError, AssertionError, KeyError):
        app.logger.error("Item_id must be a non-negative integer.")
        abort(status.HTTP_400_BAD_REQUEST, "Item_id must be a non-negative integer.")
    try:
        assert isinstance(item["item_name"], str)
    except (AssertionError, KeyError):
        app.logger.error("Item_name must be a string.")
        abort(status.HTTP_400_BAD_REQUEST, "Item_name must be a string.")
    try:
        assert isinstance(item["price"], int) or isinstance(item["price"], float)
        assert item["price"] >= 0
    except (TypeError, AssertionError, KeyError):
        app.logger.error("Price must be a non-negative integer.")
        abort(status.HTTP_400_BAD_REQUEST, "Price must be a non-negative integer.")

    if Shopcart.find_item(shopcart_id, item["item_id"]):
        item_id = item["item_id"]
        abort(
            status.HTTP_409_CONFLICT, 
            f"Shopcart with user_id '{shopcart_id}' already contains item with id '{item_id}'. Do you mean Update?"
        )
    item["user_id"] = shopcart_id
    app.logger.info(
        "Creating item %s with user_id %s, item_name %s, price %s, quantity %s...",
        item["item_id"], item["user_id"], item["item_name"], item["price"], item["quantity"]
    )    
    new_item = Shopcart()
    new_item.deserialize(item)
    new_item.create()
    return make_response(
        jsonify(new_item.serialize()), status.HTTP_201_CREATED
        )

######################################################################
# READ AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods = ["GET"])
def read_an_item(shopcart_id, item_id):
    """
    Read an item{item_id} in a certain shopcart{shopcart_id}.

    Args:
        shopcart_id (int): the shopcart which contains the item
        item_id (int): the item need to be read

    Returns:
        status code: 200 OK if successful
        message (JSON): {int: item_id, string: name, float: price, int: quantity} if successful, 
                        empty if not.
    """
    app.logger.info("Request for an item with id: %s in shopcart with id: %s", item_id, shopcart_id)
    shopcart = Shopcart.find_shopcart(shopcart_id) 
    if not shopcart:
        raise NotFound(
            "Shopcart with id '{}' was not found.".format(shopcart_id)
            )
    item = Shopcart.find_item(shopcart_id, item_id)
    if not item:
        raise NotFound(
            "Item with the id '{}' in shopcart'{}' was not found".format(item_id,shopcart_id) 
        )
    return make_response(jsonify(item.serialize()),
        status.HTTP_200_OK
        ) 

######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods = ["PUT"])
def update_items(shopcart_id, item_id):
    """
    Update an existing item in shopcart {shopcart_id}.
    Update quantity and/or price

    Args:
        shopcart_id (int): The shopcart to be updated
        body of API call (JSON): 
            quantity (int) 
            price (float/int)

            have either quantity or price, or both

    Returns:
        status code: 200 if successful, 
        404 if the requested shopcart_id or item_id does not exist,
        400 if data type errors.
        message (JSON): new item if successful, otherwise error messages
    """
    app.logger.info("Request to update an item")
    check_content_type("application/json")
    req = request.get_json()
    if not "quantity" in req.keys() and not "price" in req.keys():
        abort(status.HTTP_400_BAD_REQUEST, "Must have either quantity or price.")
    quantity = None
    price = None
    if "quantity" in req.keys():
        if not isinstance(req["quantity"], int) or req["quantity"] <= 0:
            abort(status.HTTP_400_BAD_REQUEST, "Invalid quantity.")
        else:
            quantity = req["quantity"]
    if "price" in req.keys():
        if (not isinstance(req["price"], int) and not isinstance(req["price"], float)) or req["price"] < 0:
            abort(status.HTTP_400_BAD_REQUEST, "Invalid price.")
        else:
            price = req["price"]
    
    # Make sure the shopcart exists
    shopcart = Shopcart.find_shopcart(shopcart_id)
    if not shopcart:
        abort(status.HTTP_404_NOT_FOUND, "Shopcart with id {shopcart_id} was not found.")
    # Make sure the item exists
    item = Shopcart.find_item(shopcart_id, item_id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, "item with id {item_id} was not found.")
    
    # Now proceed to update
    if quantity:
        item.quantity = quantity
        app.logger.info("item {item_id}'s quantity is changed to {quantity}")
    if price:
        item.price = price
        app.logger.info("item {item_id}'s price is changed to {price}")
    item.create()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)
    
                  
    



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
   
   
