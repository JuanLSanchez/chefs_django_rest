@load_fixture/initial_data
Feature: CRUD of recipes
  Test of create, read, update and delete recipes

  Scenario: List recipes
    When making the get request to the url '/api/recipes/'
    Then status is 200 OK
    And result size is 11

  Scenario: Create recipe without authentication
    Given  with the default recipe
    When making the post request to the url '/api/recipes/' with the body recipe
    Then status is 403 FORBIDDEN

  Scenario: Create recipe
    Given with the default recipe
    And as any user
    When making the post request to the url '/api/recipes/' with the body recipe
    Then status is 201 CREATED
    And contain id
    And the "name" attribute is equal to "Recipe"
    And the "description" attribute is equal to "Description Recipe00"