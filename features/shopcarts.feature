Feature: The shopcart store service back-end
    As a Shopcart Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

Background:
    Given a set of items in shopcarts
        | user_id | item_id | item_name | quantity | price  | hold  |
        | 1001    | 1       |  ring1    |  2       |  1998  | true  |
        | 1001    | 2       |  ring2    |  1       |  1.5   | false |
        | 1002    | 1       |  ring1    |  3       |  3     | true  |
############################################################
# CREATE SHOPCARTS
############################################################
Scenario: Create an empty shopcart which is already non-empty
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Create-Shopcart"
    Then we should see message "User with id '1001' already has a non-empty shopcart"
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "ring1" in the results
    And we should see "ring2" in the results

Scenario: Create an empty shopcart
    When we visit the "home page"
    And we enter "1003" to the text box "User_ID"
    And we press the button "Create-Shopcart"
    Then we should see message "Successfully added an empty shopcart"
    When we enter "1003" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should not see "ring1" in the results
    And we should not see "ring2" in the results

############################################################
# CLEAR SHOPCARTS
############################################################
Scenario: Clear a non-empty shopcart Case 1
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    Then we should see message "Successfully cleared the shopcart"
    When we press the button "Retrieve"
    Then we should not see "ring1" in the results
    And we should not see "ring2" in the results

Scenario: Clear a non-empty shopcart Case 2
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    Then we should see message "Successfully cleared the shopcart"
    When we enter "1002" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "ring1" in the results

############################################################
# RETRIEVE SHOPCARTS
############################################################
Scenario: Retrieve a non-empty shopcart
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see message "Successfully retrieved the shopcart"
    And we should see "ring1" in the results
    And we should see "ring2" in the results
    And we should not see "3" in the results

Scenario: Retrieve an empty shopcart
    When we visit the "home page"
    And we enter "1003" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see message "Successfully retrieved the shopcart"
    And we should not see "ring1" in the results
    And we should not see "ring2" in the results

############################################################
# LIST SHOPCARTS
############################################################ 
Scenario: List all shopcarts
    When we visit the "home page"
    And we press the button "List-All-Shopcarts"
    Then we should see message "Successfully listed all the shopcarts"
    And we should see "1001" in the shopcarts table
    And we should see "1002" in the shopcarts table

Scenario: List shopcarts when there are none
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    And we enter "1002" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    And we press the button "List-All-Shopcarts"
    Then we should see message "Successfully listed all the shopcarts"
    And we should not see "1001" in the shopcarts table
    And we should not see "1002" in the shopcarts table

############################################################
# GET ITEMS
############################################################
Scenario: Get items 
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID" 
    And we enter "1" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should see "ring1" in the results
    Then we should see "1998" in the results
    Then we should not see "ring2" in the results
    Then we should not see "1.5" in the results
    Then we should not see "3" in the results

Scenario: Get Items None Case 1
    When we visit the "home page"
    And we enter "1002" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should not see "ring1" in the results
    Then we should not see "ring2" in the results
    Then we should not see "1998" in the results
    Then we should not see "1.5" in the results
    Then we should not see "3" in the results
    Then we should not see "false" in the results

Scenario: Get Items None Case 2
    When we visit the "home page"
    And we enter "1003" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should not see "ring1" in the results
    Then we should not see "ring2" in the results
    Then we should not see "1998" in the results
    Then we should not see "1.5" in the results
    Then we should not see "3" in the results
    Then we should not see "false" in the results

############################################################
# HOLD ITEMS
############################################################
Scenario: Hold Items Case 1
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Hold-For-Later"
    Then we should see message "Successfully put item on hold"
    When we enter "1001" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should not see "false" in the results
    And we should see "true" in the results

Scenario: Hold Items Case 2
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Hold-For-Later"
    Then we should see message "Successfully put item on hold"
    When we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should not see "false" in the results
    And we should see "true" in the results

Scenario: Hold Items Invalid
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "true" to the text box "Item_ID"
    And we press the button "Hold-For-Later"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results

############################################################
# RESUME ITEMS
############################################################
Scenario: Resume item on held item
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Resume-For-Purchase"
    Then we should see message "Successfully resumed item for purchase"
    When we enter "1001" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should see "false" in the results
    And we should not see "true" in the results

Scenario: Resume item on item already in cart
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Resume-For-Purchase"
    Then we should see message "Successfully resumed item for purchase"
    When we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Get-Item"
    Then we should see "false" in the results
    And we should not see "true" in the results


Scenario: Resume item invalid item id
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we enter "true" to the text box "Item_ID"
    And we press the button "Resume-For-Purchase"
    Then we should not see "false" in the results
    And we should not see "true" in the results

############################################################
# DELETE ITEMS
############################################################
Scenario: Delete an exist item
    When we enter "1001" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Remove"
    Then we should see message "Successfully deleted an item"
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998" in the results
    And we should not see "2 ring2 1 1.5" in the results
    And we should not see "1 ring1 3 3" in the results

Scenario: Delete an item when the shopcart doesn't exist
    When we enter "1003" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we press the button "Remove"
    Then we should see message "Successfully deleted an item"
    When we enter "1003" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should not see "1 ring1 2 1998" in the results
    And we should not see "2 ring2 1 1.5" in the results
    And we should not see "1 ring1 3 3" in the results

    
Scenario: Delete an item that doesn't exist
    When we enter "1002" to the text box "User_ID"
    And we enter "2" to the text box "Item_ID"
    And we press the button "Remove"
    Then we should see message "Successfully deleted an item"
    When we enter "1002" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should not see "1 ring1 2 1998" in the results
    And we should not see "2 ring2 1 1.5" in the results
    And we should see "1 ring1 3 3" in the results

############################################################
# ADD AN ITEM IN SHOPCARTS
############################################################
Scenario: Add an exist item
    When we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we enter "ring" to the text box "Item_Name"
    And we enter "1" to the text box "Quantity"
    And we enter "2" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Shopcart with user_id '1001' already contains item with id '1'. Do you mean Update?"
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results
    And we should not see "1 ring1 3 3 true" in the results
    And we should not see "1 ring 1 2 false" in the results

Scenario: Add an item successfully Case 1
    When we enter "1001" to the text box "User_ID"
    And we enter "3" to the text box "Item_ID"
    And we enter "ring3" to the text box "Item_Name"
    And we enter "1" to the text box "Quantity"
    And we enter "2.5" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Successfully added an Item"
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results
    And we should see "3 ring3 1 2.5 false" in the results
    And we should not see "1 ring1 3 2.5 true" in the results

Scenario: Add an item successfully Case 2
    When we enter "1003" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we enter "ring" to the text box "Item_Name"
    And we enter "1" to the text box "Quantity"
    And we enter "2" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Successfully added an Item"
    When we enter "1003" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should not see "1 ring1 2 1998 true" in the results
    And we should not see "2 ring2 1 1.5 false" in the results
    And we should not see "1 ring1 3 3 true" in the results
    And we should see "1 ring 1 2 false" in the results

Scenario: Add an item without a vaild Item_ID
    When we enter "1001" to the text box "User_ID"
    And we enter "-1" to the text box "Item_ID"
    And we enter "ring" to the text box "Item_Name"
    And we enter "1" to the text box "Quantity"
    And we enter "2" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Item_id must be a non-negative integer."
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results
    And we should not see "1 ring1 3 3 true" in the results
    And we should not see "-1 ring 1 2 false" in the results

Scenario: Add an item without a vaild Quantity
    When we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "User_ID"
    And we enter "ring" to the text box "Item_Name"
    And we enter "0" to the text box "Quantity"
    And we enter "2" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Quantity must be a positive integer."
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results
    And we should not see "1 ring1 3 3 true" in the results
    And we should not see "1 ring 0 2 false" in the results

Scenario: Add an item without a vaild Price
    When we enter "1001" to the text box "User_ID"
    And we enter "1" to the text box "Item_ID"
    And we enter "ring" to the text box "Item_Name"
    And we enter "1" to the text box "Quantity"
    And we enter "-1" to the text box "Price"
    And we press the button "Add-To-Shopcart"
    Then we should see message "Price must be a positive int or float."
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "1 ring1 2 1998 true" in the results
    And we should see "2 ring2 1 1.5 false" in the results
    And we should not see "1 ring1 3 3 true" in the results
    And we should not see "1 ring 1 -1 false" in the results

