Feature: Registering masterpiece in availability service

  Scenario: Registering masterpiece
    Given masterpiece
    When merchant is publishing masterpiece
    Then masterpiece is available
