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
    When I visit the "home page"
    And I enter "1001" to the text box "User_ID"
    And I press the button "Create-Shopcart"
    Then I should see status code 400
    And I should see message "User with id '1001' already has a non-empty shopcart."
    When I enter "1001" to the text box "User_ID"
    And I press the button "Retrieve"
    Then I should see "ring1" in the results
    And I should see "ring2" in the results

Scenario: Create an empty Shopcart
    When I visit the "home page"
    And I enter "1003" to the text box "User_ID"
    And I press the button "Create-Shopcart"
    Then I should see message "Successfully Added an empty Shopcart"
    When I enter "1003" to the text box "User_ID"
    And I press the button "Retrieve"
    Then I should not see "ring1" in the results
    And I should not see "ring2" in the results

Scenario: List all shopcarts
    When I visit the "home page"
    And  I press the button "List All Shopcarts"
    Then I should see message "Successfully list all the shopcarts"
    And I should see "1001" in the shopcart table
    And I should see "1002" in the shopcart table