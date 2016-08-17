Feature: Testing
  Testing the features

  Scenario Outline: Scenario 1
    Given x equals <x>
    And y equals <y>
    When sum x and y
    Then result sum equals <sum>
    Examples:
      | x | y | sum |
      | 1 | 2 | 3   |
      | 2 | 2 | 4   |
      | 2 | 3 | 5   |
