Feature: Blocking masterpiece

  Background:
    Given published masterpiece

  Scenario: Buying masterpiece
    Given masterpiece was reserved
    When masterpiece was bought
    Then masterpiece is reserved as permanent block

  Scenario: Buying not reserved masterpiece
    When buying not reserved masterpiece
    Then not reserved masterpiece is reserved as permanent block
