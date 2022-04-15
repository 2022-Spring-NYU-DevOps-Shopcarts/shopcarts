## Shopcarts Service
Version: 1.1

Resource URLs: ```/shopcarts```, ```/shopcarts/<user-id>```, ```/shopcarts/<user-id>/items```, ```/shopcarts/<user-id>/items/<item-id>```

Allows different users to store items in their shopcarts.
Run via ```honcho start```.
Test via ```nosetests``` and (after starting local server) ```behave```.

### Usage: 
    POST   on /shopcarts: creates a new empty shopcart with given <user-id>.
    
    POST   on /shopcarts: creates a new shopcart at given <user-id> with a single item
        Expects JSON body data:
            user_id: int
            item_id: int
            item_name: string
            quantity: int
            price: float/int
      
    POST   on /shopcarts: creates a new shopcart at given <user-id> with a list of items.
        Expects JSON body data:
            user_id: int
            items: a list of: 
                              item_id: int
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
            
    GET    on /shopcarts/<user-id>/items/<item_id>: retrieves an <item-id> item in a certain <user-id> shopcart
    
    PUT    on /shopcarts/<user-id>/items/<item_id>: updates price and/or quantity of an existing item in shopcart <shopcart-id>
        Expects JSON body data:
            one or both of below:
                quantity: int
                price: float/int
            
    DELETE on /shopcarts/<user-id>/items/<item_id>: deletes an <item_id> item in a certain <user-id> shopcart
    
### To be implemented:
    PUT    on /shopcarts/<user-id>: batch update items in <user-id> shopcart.
        Expects JSON body data:
            tbd
    
