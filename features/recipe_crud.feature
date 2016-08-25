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
    And save the number of recipe of the owner of 'recipe' in 'other_user_recipes_old'
    When modify the 'owner' id of the object body 'recipe' by the principal id
    And modify the string attribute 'name' of the object body 'recipe' by 'Test Name'
    And modify the attribute 'id' of the object body 'recipe' by the attribute of object 'recipe1'
    And making the put request to the url '/api/recipes/' with the attribute as id 'id' of 'recipe' and the body 'recipe'
    Then status is 200 OK
    And the 'id' attribute is equals to the 'id' attribute of the 'recipe1' object
    And the 'owner' attribute is equals to the 'owner' attribute of the 'recipe1' object
    And save the number of recipe of the owner of 'recipe1' in 'principal_recipes_new'
    And save the number of recipe of the owner of 'recipe' in 'other_user_recipes_new'
    And the 'principal_recipes_old' variable is equals to th 'principal_recipes_new' variable
    And the 'other_user_recipes_old' variable is equals to th 'other_user_recipes_new' variable

  Scenario: Update recipe with the id modified
    Given like a user with recipes
    And with any recipe of the user as 'recipe1'
    And with any recipe of other user as 'recipe'
    And save the number of recipe of the owner of 'recipe1' in 'principal_recipes_old'
    And save the number of recipe of the owner of 'recipe' in 'other_user_recipes_old'
    When modify the string attribute 'id' of the object body 'recipe' by 'Test Name'
    And making the put request to the url '/api/recipes/' with the attribute as id 'id' of 'recipe1' and the body 'recipe'
    Then status code is 400