## name: Shopcarts Service
version: 1.0

resource URLs: /shopcarts/<user-id>

Allows different users to store items in their shopcarts.

### Usage: 
    POST   on /shopcarts: creates new shopcart based on body data
    GET    on /shopcarts: returns list of all shopcarts
    PUT    on /shopcarts/<user-id>: add/delete items in <user-id> shopcart
    GET    on /shopcarts/<user-id>: returns items in <user-id> shopcart
    DELETE on /shopcarts/<user-id>: deletes <user-id> shopcart
