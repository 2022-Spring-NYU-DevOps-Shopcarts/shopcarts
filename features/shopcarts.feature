Feature: The shopcart store service back-end
    As a Shopcart Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

Background:
    Given a set of items in shopcarts
        | user_id | item_id | item_name | quantity | price  |
        | 1001    | 1       |  ring1    |  2       |  1998  |
        | 1001    | 2       |  ring2    |  1       |  1.5   |
        | 1002    | 1       |  ring1    |  3       |  3     |

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
Scenario: Clear a non-empty shopcart
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    Then we should see message "Successfully cleared the shopcart"
    When we press the button "Retrieve"
    Then we should not see "ring1" in the results
    And we should not see "ring2" in the results

Scenario: Clear a non-empty shopcart
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

