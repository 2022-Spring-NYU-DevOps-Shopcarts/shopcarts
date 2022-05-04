"""
name: Shopcarts Service
version: 1.0
Allows different users to store items in their shopcarts.
See http://nyu-shopcart-service-sp2203.us-south.cf.appdomain.cloud/apidocs
for documentation.

"""
from attr import validate
from werkzeug.exceptions import NotFound
from flask import jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Shopcart, DataValidationError, DatabaseConnectionError
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
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Shopcart REST API Service',
          description='This is a Shopcart server.',
          default='shopcarts',
          default_label='Shopcart operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/'
         )

create_item_model = api.model('Item', {
    'item_id': fields.Integer(required=True,
                              description='The ID of the Item',
                              min = 0,
                              example = 1),
    'item_name': fields.String(required=True,
                               description='The name of the Item'),
    'quantity': fields.Integer(required=True,
                               description='The quantity of the Item',
                               min = 1),
    'price': fields.Float(required=True,
                          description='The price of the Item',
                          min = 0,
                          exclusiveMin = True),
    'hold': fields.Boolean(required=True,
                            description='The holding status of the Item')
})

# Define the model so that the docs reflect what can be sent
create_shopcart_model = api.model('Shopcart', {
    'user_id': fields.Integer(required=True,
                              description='The ID of the user',
                              min = 0),
    'item_id': fields.Integer(description='The ID of the item',
                              min = 0),
    'item_name': fields.String(description='The name of the item'),
    'quantity': fields.Integer(description='The quantity of the Item',
                               min = 1),
    'price': fields.Float(description='The price of the Item',
                          min = 0,
                          exclusiveMin = True),
    'hold': fields.Boolean(description='The holding status of the Item'),
    'items': fields.List(fields.Nested(create_item_model),
                         description='The list of Items (use for multiple items)')
})

item_model = api.model('ItemModel', {
    'user_id': fields.Integer(readOnly=True,
                              description='The ID of the User',
                              min = 0),
    'item_id': fields.Integer(readOnly=True,
                              description='The ID of the Item',
                              min = 0),
    'item_name': fields.String(readOnly=True,
                               description='The name of the Item'),
    'quantity': fields.Integer(description='The quantity of the Item',
                               min = 1),
    'price': fields.Float(description='The price of the Item',
                          min = 0,
                          exclusiveMin = True),
    'hold': fields.Boolean(description='The holding status of the Item')
})

update_item_model = api.model('ItemModel', {
    'quantity': fields.Integer(description='The quantity of the Item',
                               min = 1),
    'price': fields.Float(description='The price of the Item',
                          min = 0,
                          exclusiveMin = True)       
})

update_item_model = api.model('ItemModel', {
    'quantity': fields.Integer(description='The quantity of the Item',
                               min = 1),
    'price': fields.Float(description='The price of the Item',
                          min = 0,
                          exclusiveMin = True)       
})

list_shopcart_model = api.model('ShopcartModel', {
    'user_id': fields.Integer(readOnly=True,
                              description='The ID of the User')
})

# query string arguments
shopcart_args = reqparse.RequestParser()
shopcart_args.add_argument('item-id', type=int, required=False, help='Optional, to list shopcarts containing the item id')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

# @api.errorhandler(DatabaseConnectionError)
# def database_connection_error(error):
#     """ Handles Database Errors from connection attempts """
#     message = str(error)
#     app.logger.critical(message)
#     return {
#         'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
#         'error': 'Service Unavailable',
#         'message': message
#     }, status.HTTP_503_SERVICE_UNAVAILABLE

######################################################################
#  PATH: /shopcarts
######################################################################
@api.route('/shopcarts', strict_slashes=False)
class ShopcartCollection(Resource):

    ######################################################################
    # ADD A NEW SHOPCART
    ######################################################################
    @api.doc('create_shopcarts')
    @api.response(400, 'Invalid posted data')
    @api.response(409, 'Non-empty shopcart already exists at this id')
    @api.response(201, 'Created shopcart')
    @api.expect(create_shopcart_model)
    @api.marshal_list_with(item_model, code=201)
    def post(self):
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
                status.HTTP_409_CONFLICT, 
                f"User with id '{user_id}' already has a non-empty shopcart.",
            )
        
        shopcarts = []
        shopcarts_deserialize = []
        if "items" in req.keys():
            shopcarts = req["items"]
        if "item_id" in req.keys():
            shopcarts.append(req)
        for s in shopcarts:
            s["user_id"] = req["user_id"]
            shopcart = Shopcart()
            shopcart.deserialize(s)
            shopcarts_deserialize.append(shopcart)
        for s in shopcarts_deserialize:
            if Shopcart.find_item(req["user_id"], s.item_id):
                shopcart = Shopcart.find_shopcart(req["user_id"]) 
                if shopcart:
                    for item in shopcart:
                        item.delete()
                abort(
                status.HTTP_400_BAD_REQUEST, 
                f"Item with id '{s.item_id}' appears more than once in the data.",
            )
            s.create()
        location_url = api.url_for(ShopcartResource, user_id=req["user_id"], _external=True)
        app.logger.info("Shopcart with ID [%s] created.", req["user_id"])
        results = [shopcart.serialize() for shopcart in shopcarts_deserialize]
        return results, status.HTTP_201_CREATED, {"Location": location_url}

    ######################################################################
    # LIST ALL SHOPCARTS / QUERY ALL SHOPCARTS CONTAINING AN ITEM
    ######################################################################
    @api.doc('list_shopcarts')
    @api.expect(shopcart_args, validate=True)
    @api.response(200, 'Listed all shopcarts')
    @api.marshal_list_with(list_shopcart_model)
    def get(self):
        """Returns all of the Shopcarts OR only those with the given item-id"""
        app.logger.info("Request for shopcart list")
        args = shopcart_args.parse_args()
        if args['item-id']:
            app.logger.info("Filtering shopcarts by item id %s", args['item-id'])
            shopcarts = Shopcart.query_by_item_id(args['item-id'])
        else:
            app.logger.info("Returning unfiltered shopcart lists")
            shopcarts = Shopcart.all_shopcart()

        results = [dict(shopcart) for shopcart in shopcarts]
        app.logger.info("Returning %d shopcarts", len(results))
        return results, status.HTTP_200_OK



######################################################################
#  PATH: /shopcarts/{id}
######################################################################
@api.route('/shopcarts/<int:user_id>', strict_slashes=False)
@api.param('user_id', 'The User identifier')
class ShopcartResource(Resource):

    ######################################################################
    # RETRIEVE A SHOPCART
    ######################################################################
    @api.doc('get_shopcarts')
    @api.marshal_list_with(item_model)
    @api.response(200, 'Retrieved shopcart')
    def get(self, user_id):
        """
        Retrieve a single Shopcart
        This endpoint will return a Shopcart based on its id
        """
        app.logger.info("Request for shopcart with id: %s", user_id)
        
        #This is the list of shopcarts which user_id == shopcart_id
        shopcart = Shopcart.find_shopcart(user_id)         
        if not shopcart:
            return [], status.HTTP_200_OK 

        app.logger.info("Returning shopcart: %s", user_id)
        #As 1 user is attached to 1 user_id
        return [sc.serialize() for sc in shopcart], status.HTTP_200_OK


    ######################################################################
    # DELETE A SHOPCART
    ######################################################################
    @api.doc('delete_shopcarts')
    @api.response(204, 'No content')
    def delete(self, user_id):
        """
        Delete a single Shopcart
        This endpoint will return a Shopcart based on its id
        """
        app.logger.info("Request to delete shopcart with id: %s", user_id)
        
        shopcart = Shopcart.find_shopcart(user_id) 
        if shopcart:
            for item in shopcart:
                item.delete()
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /shopcarts/{id}/items
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/items')
@api.param('shopcart_id', 'The Shopcart identifier')
class ItemCollectionResource(Resource):

    ######################################################################
    # CREATE AN ITEM
    ######################################################################
    @api.doc('create_items')
    @api.response(201, 'created')
    @api.response(409, 'item already in cart')
    @api.response(400, 'invalid attributes')
    @api.expect(create_item_model)
    @api.marshal_with(item_model)
    def post(self, shopcart_id):
        """
        Create new item in shopcart {shopcart_id}.
        This endpoint will create an item based the data in the body that is posted
        """
        check_content_type("application/json")
        item = request.get_json()
        app.logger.info("Received item %s...", item)

        try:
            assert isinstance(item["quantity"], int)
            assert item["quantity"] > 0
        except:
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
            assert item["price"] > 0
        except (TypeError, AssertionError, KeyError):
            app.logger.error("Price must be a positive int or float.")
            abort(status.HTTP_400_BAD_REQUEST, "Price must be a positive int or float.")

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
        return new_item.serialize(), status.HTTP_201_CREATED
            

######################################################################
#  PATH: /shopcarts/{id}/items/{id}
######################################################################
@api.route('/shopcarts/<int:shopcart_id>/items/<int:item_id>')
@api.param('shopcart_id', 'The Shopcart identifier')
@api.param('item_id', 'The item identifier')

class ItemResource(Resource):

    ######################################################################
    # READ AN ITEM
    ######################################################################
    @api.doc('get_items')
    @api.response(404, 'not found')
    @api.response(200, 'item retrieved')
    @api.marshal_with(item_model)

    def get(self, shopcart_id, item_id):
        """
        Read an item{item_id} in a certain shopcart{shopcart_id}.
        This endpoint will read an item based on the shopcart_id and item_id argument in the url
        """

        app.logger.info("Request for an item with id: %s in shopcart with id: %s", item_id, shopcart_id)

        shopcart = Shopcart.find_shopcart(shopcart_id) 
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND,
                "Shopcart with id '{}' was not found.".format(shopcart_id)
                )
        item = Shopcart.find_item(shopcart_id, item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND,
                "Item with the id '{}' in shopcart'{}' was not found".format(item_id,shopcart_id) 
            )
        return item.serialize(), status.HTTP_200_OK


    ######################################################################
    # UPDATE AN ITEM
    ######################################################################
    @api.doc('update_items')
    @api.response(404, 'not found')
    @api.response(400, 'invalid quantity or price')
    @api.response(200, 'item updated')
    @api.expect(update_item_model)
    @api.marshal_with(item_model)

    def put(self, shopcart_id, item_id):
        """
        Update an item{item_id} in a certain shopcart{shopcart_id}.
        This endpoint will update an item based on the shopcart_id and item_id argument in the url
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
            abort(status.HTTP_404_NOT_FOUND, f"Shopcart with id {shopcart_id} was not found.")
        # Make sure the item exists
        item = Shopcart.find_item(shopcart_id, item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"item with id {item_id} was not found.")
        
        # Now proceed to update
        if quantity:
            item.quantity = quantity
            app.logger.info(f"item {item_id}'s quantity is changed to {quantity}")
        if price != None and price >= 0:
            item.price = price
            app.logger.info(f"item {item_id}'s price is changed to {price}")
        item.create()
        return item.serialize(), status.HTTP_200_OK


    ######################################################################
    # DELETE AN ITEM
    ######################################################################
    @api.doc('delete_items')
    @api.response(404, 'not found')
    @api.response(204, 'deleted')

    def delete(self, shopcart_id, item_id):
        """
        Delete an item{item_id} in a certain shopcart{shopcart_id}.
        This endpoint will delete an item based on the shopcart_id and item_id argument in the url
        """

        app.logger.info("Attempting to delete item %s from shopcart %s...", item_id, shopcart_id)
        try:
            item = Shopcart.find_item_or_404(shopcart_id, item_id)
            item.delete()
        except NotFound:
            pass
        app.logger.info("Making 204 response...")
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /shopcarts/{id}/items/{item_id}/hold
######################################################################
@api.route('/shopcarts/<int:user_id>/items/<int:item_id>/hold', strict_slashes=False)
@api.param('user_id', 'The User identifier')
@api.param('item_id', 'The Item identifier')
class HoldResource(Resource):
    """
    HoldResource class

    Allows the holding status changes of a single Item
    PUT /shopcarts/{id}/items/{item_id}/hold - Updates an Item's holding status to True
    """

	######################################################################
	# HOLD AN ITEM
	######################################################################
    @api.doc("hold_items")
    @api.response(404, 'Shopcart or Item not found')
    @api.response(200, 'Item put on hold')
    @api.marshal_list_with(item_model)
    def put(self, user_id, item_id):
        shopcart = Shopcart.find_shopcart(user_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND, f"Shopcart with id {user_id} was not found.")
        # Make sure the item exists
        item = Shopcart.find_item(user_id, item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"item with id {item_id} was not found.")
        item.hold = True
        app.logger.info("Attempting to hold item %s from shopcart %s...", item_id, user_id)
        app.logger.info("Making 200 response...")
        return make_response(jsonify(item.serialize()), status.HTTP_200_OK)
        
######################################################################
#  PATH: /shopcarts/{id}/items/{item_id}/resume
######################################################################
@api.route('/shopcarts/<int:user_id>/items/<int:item_id>/resume')
@api.param('user_id', 'The User identifier')
@api.param('item_id', 'The Item identifier')
class ResumeResource(Resource):
    """
    ResumeResource class

    Allows the holding status changes of a single Item
    PUT /shopcarts/{id}/items/{item_id}/hold - Updates an Item's holding status to False
    """

    ######################################################################
	# RESUME AN ITEM
	######################################################################
    @api.doc("resume_items")
    @api.response(404, 'Shopcart or Item not found')
    @api.response(200, 'Item resumed')
    @api.marshal_list_with(item_model)
    def put(self, user_id, item_id):
        """
        Resume item in shopcart {shopcart_id} with item_id {item_id}
            from held (will be ordered when user checks out the shopcart)
        Args:
            shopcart_id (int): The shopcart containing the relevant item
            item_id (int): The item to be deleted
        Returns:
            status code: 200 if successful, 
            404 if the requested shopcart_id or item_id does not exist,
            400 if data type errors.
            message (JSON): item if successful, otherwise error messages
        """   
        app.logger.info("Attempting to resume item %s from shopcart %s...", item_id, user_id)
        shopcart = Shopcart.find_shopcart(user_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND, f"Shopcart with id {user_id} was not found.")
        # Make sure the item exists
        item = Shopcart.find_item(user_id, item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"item with id {item_id} was not found.")
        item.hold = False
        app.logger.info("Making 200 response...")
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
   
   
