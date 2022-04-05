## Shopcarts Service
Version: 1.0

Resource URLs: ```/shopcarts``` and ```/shopcarts/<user-id>```

Allows different users to store items in their shopcarts.
Execute via ```flask run -h 0.0.0.0 -p 8000```.
Test via ```nosetests```.

### Usage: 
    POST   on /shopcarts: creates a new empty shopcart with given <user-id>.
    POST   on /shopcarts: creates a new shopcart with given <user-id> and a list of items.
        Expects JSON body data of single item:
            item_id: int
            user_id: int
            item_name: string
            quantity: int
            price: float/int
    GET    on /shopcarts: returns all of the shopcarts.
    GET    on /shopcarts/<user-id>: returns items in <user-id> shopcart.
    DELETE on /shopcarts/<user-id>: deletes <user-id> shopcart.
    POST   on /shopcarts/<user-id>/items: creates new item in <user-id> shopcart.
        Expects JSON body data:
            item_id: int
            quantity: int 
            item_name: string
            price: float/int
    GET    on /shopcarts/<user-id>/items/<item_id>: reads an <item_id> item in a certain <user-id> shopcart
    PUT    on /shopcarts/<user-id>/items/<item_id>: updates price and/or quantity of an existing item in shopcart {shopcart_id}
        Expects JSON body data:
            quantity: int
            price: float/int
    DELETE on /shopcarts/<user-id>/items/<item_id>: deletes an <item_id> item in a certain <user-id> shopcart
### To be fixed:
    PUT    on /shopcarts/<user-id>: change item quantities in <user-id> shopcart. 
        Expects JSON body data:
            item_id: int (not -1)
            item_name: string
            quantity: int
            price: float/int
    
