## Shopcarts Service
Version: 1.0

Resource URLs: ```/shopcarts``` and ```/shopcarts/<user-id>```

Allows different users to store items in their shopcarts.
Execute via ```flask run -h 0.0.0.0 -p 8000```.
Test via ```nosetests```.

### Usage: 
    POST   on /shopcarts: creates new shopcart.
        Expects JSON body data:
            item_id: -1
            user_id: int
            item_name: string
            quantity: int
            price: float
    GET    on /shopcarts: returns list of all shopcarts
    PUT    on /shopcarts/<user-id>: change item quantities in <user-id> shopcart.
        Expects JSON body data:
            item_id: int (not -1)
            item_name: string
            quantity: int
            price: float
    GET    on /shopcarts/<user-id>: returns items in <user-id> shopcart
    DELETE on /shopcarts/<user-id>: deletes <user-id> shopcart
