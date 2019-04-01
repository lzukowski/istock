Feature: Blocking masterpiece

  Background:
    Given published masterpiece

  Scenario: Buying masterpiece
    When masterpiece was reserved
    And masterpiece was bought
    Then masterpiece is reserved as permanent block
