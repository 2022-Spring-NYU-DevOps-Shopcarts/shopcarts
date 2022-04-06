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

Scenario: Create an empty Shopcart which is already non-empty
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Create-Shopcart"
    Then we should see status code 400
    And we should see message "User with id '1001' already has a non-empty shopcart."
    When we enter "1001" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "ring1" in the results
    And we should see "ring2" in the results

Scenario: Create an empty Shopcart
    When we visit the "home page"
    And we enter "1003" to the text box "User_ID"
    And we press the button "Create-Shopcart"
    Then we should see message "Successfully Added an empty Shopcart"
    When we enter "1003" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should not see "ring1" in the results
    And we should not see "ring2" in the results

Scenario: Clear a non-empty Shopcart
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    Then we should see message "Successfully cleared the shopcart"
    When we press the button "Retrieve"
    Then we should not see "ring1" in the results
    And we should not see "ring2" in the results

Scenario: Clear a non-empty Shopcart
    When we visit the "home page"
    And we enter "1001" to the text box "User_ID"
    And we press the button "Clear-Shopcart"
    Then we should see message "Successfully cleared the shopcart"
    When we enter "1002" to the text box "User_ID"
    And we press the button "Retrieve"
    Then we should see "ring1" in the results
    
Scenario: List all shopcarts
    When we visit the "home page"
    And  we press the button "List All Shopcarts"
    Then we should see message "Successfully list all the shopcarts"
    And we should see "1001" in the shopcart table
    And we should see "1002" in the shopcart table