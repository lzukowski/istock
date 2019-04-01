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

  Scenario Outline: Buying masterpiece reserved by other buyer
    Given masterpiece was reserved
    When other buyer wants to buy <variant> of masterpiece
    Then reservation is rejected
    Examples:
      | variant       |
      | same variant  |
      | other variant |

  Scenario: Buying masterpiece which reservation expired
    Given masterpiece with expired reservation
    When other buyer wants to buy masterpiece
    Then masterpiece is reserved as permanent block

  Scenario Outline: Buying other variation for already blocked masterpiece
    Given purchased masterpiece
    When same buyer wants to <action> other variation of masterpiece
    Then succeed with permanent variation block
    Examples:
      | action  |
      | reserve |
      | buy     |
