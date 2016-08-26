@load_fixture/initial_data
Feature: CRUD of recipes
  Test of create, read, update and delete recipes

  Scenario: List recipes
    When making the get request to the url '/api/recipes/'
    Then status is 200 OK
    And result size in page is 10
    And total result in page is 11

  Scenario: Details of one recipe
    When making the get request to the url '/api/recipes/1/'
    Then status is 200 OK

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
    And the 'name' attribute is equal to 'Recipe'
    And the 'description' attribute is equal to 'Description Recipe00'

  Scenario: Update recipe
    Given like a user with recipes
    And with any recipe of the user as 'recipe'
    When modify the string attribute 'name' of the object body 'recipe' by 'Test Name'
    And modify the string attribute 'description' of the object body 'recipe' by 'Test Description'
    And making the put request to the url '/api/recipes/' with the attribute 'id' and the body 'recipe'
    Then status is 200 OK
    And the 'name' attribute is equal to 'Test Name'
    And the 'description' attribute is equal to 'Test Description'

  Scenario: Update recipe with other user
    Given like a user without recipes
    And with any recipe as 'recipe'
    When making the put request to the url '/api/recipes/' with the attribute 'id' and the body 'recipe'
    Then status is 403 FORBIDDEN

  Scenario: Update recipe with the user modified of other user
    Given like a user with recipes
    And with any recipe of the user as 'recipe1'
    And with any recipe of other user as 'recipe'
    And save the number of recipe of the owner of 'recipe1' in 'principal_recipes_old'
    When modify the 'owner' id of the object body 'recipe' by the principal id
    And making the put request to the url '/api/recipes/' with the attribute as id 'id' of 'recipe' and the body 'recipe1'
    Then status is 403 FORBIDDEN

  Scenario: Update recipe with the id modified
    Given like a user with recipes
    And with any recipe of the user as 'recipe1'
    And with any recipe of other user as 'recipe'
    And save the number of recipe of the owner of 'recipe1' in 'principal_recipes_old'
    And save the number of recipe of the owner of 'recipe' in 'other_user_recipes_old'
    When modify the string attribute 'id' of the object body 'recipe' by 'Test Name'
    And making the put request to the url '/api/recipes/' with the attribute as id 'id' of 'recipe1' and the body 'recipe'
    Then status code is 400

  Scenario: Delete a recipe without authentication
    When making the delete request to the url '/api/recipes/1/'
    Then status is 403 FORBIDDEN

  Scenario: Delete a recipe with the owner
    Given like a user with recipes
    And with any recipe of the user as 'recipe'
    When making the delete request with object, to the url '/api/recipes/' with the 'id' of the object 'recipe'
    Then status is 204 NOT CONTENT

  Scenario: Delete a recipe with other owner
    Given like a user with recipes
    And with any recipe of other user as 'recipe'
    When making the delete request with object, to the url '/api/recipes/' with the 'id' of the object 'recipe'
    Then status is 403 FORBIDDEN