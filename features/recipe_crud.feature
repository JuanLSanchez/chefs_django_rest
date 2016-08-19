@load_fixture/initial_data
Feature: CRUD of recipes
  Test of create, read, update and delete recipes

  Scenario: List recipes
    When making the get request to the url '/api/recipes/'
    Then status is 200 OK
    And result size in page is 10
    And total result in page is 11

  Scenario: Create recipe without authentication
    Given  with the default recipe as 'recipe'
    When making the post request to the url '/api/recipes/' with the body recipe
    Then status is 403 FORBIDDEN

  Scenario: Create recipe
    Given with the default recipe as 'recipe'
    And like any user
    When making the post request to the url '/api/recipes/' with the body recipe
    Then status is 201 CREATED
    And contain id
    And the "name" attribute is equal to "Recipe"
    And the "description" attribute is equal to "Description Recipe00"

  Scenario: Update recipe
    Given like a user with recipes
    And with any recipe of the user as 'recipe'
    When modify the string attribute 'name' of the object body 'recipe' by 'Test Name'
    And modify the string attribute 'description' of the object body 'recipe' by 'Test Description'
    And making the put request to the url '/api/recipes/' with the attribute 'id' and the body 'recipe'
    Then status is 200 OK
    And the "name" attribute is equal to "Test Name"
    And the "description" attribute is equal to "Test Description"

  Scenario: Update recipe with other user
    Given like a user without recipes
    And with any recipe as 'recipe'
    When making the put request to the url '/api/recipes/' with the attribute 'id' and the body 'recipe'
    Then status is 403 FORBIDDEN

  Scenario: Update recipe with the user modified of other user
    Given like a user with recipes
    And with any recipe of the user as 'recipe1'
    And with any recipe of other user as 'recipe'
    When modify the 'owner' id of the object body 'recipe' by the principal id
    And modify the string attribute 'name' of the object body 'recipe' by 'Test Name'
    And making the put request to the url '/api/recipes/' with the attribute as id 'id' of 'recipe1' and the body 'recipe'
    Then status is 403 FORBIDDEN
