Feature: The Shopcart service back-end
    As a Shop Owner
    I need a RESTful shopcart service
    So that I can keep track of all customers' shopcarts

Background:
    Given the following pets
        | Item ID   | Item Name | Quantity  | Price     |
        | 1001      | ring01    | 2         | 2998      |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Search for dogs
    When I visit the "Home Page"
    And I set the "User ID" to "1080"
    And I press the "Retrive" button
    Then I should see "1001" in the results

Scenario: Add an Item
    When I visit the "Home Page"
    And I set the "User ID" to "1080"
    And I set the "Item ID" to "1002"
    And I set the "Quantity" to "3998"
    And I press the "Add to Shop Cart" button
    Then I should see the message "Success"
