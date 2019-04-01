Feature: Reserving masterpiece

  Scenario: Reserving masterpiece
    Given published masterpiece
    When customer reserve variant of masterpiece
    Then masterpiece is reserved

  Scenario: Reserving masterpiece variant for second time
    Given reserved masterpiece variant
    When owner reserve variant of masterpiece for second time
    Then reservation is rejected

  Scenario: Reserving masterpiece variant when other variation was already reserved
    Given reserved masterpiece variant
    When other buyer reserve other variant of masterpiece
    Then reservation is rejected

  Scenario: Reserving masterpiece variant when previous reservation expires
    Given expired masterpiece variant reservation
    When customer reserve variant of masterpiece
    Then masterpiece is reserved
