Feature:
  User provides shortened url to be redirected to original url

  Scenario: User provides stored short url and is redirected
    Given stored url is "http://www.google.com"
    When I get "7WRqMzTKiR_TRn2xMTchQA=="
    Then the response status code is 302
    And the redirection is to "http://www.google.com"

  Scenario: User provides a short url that is not found
    When I get "aaabbbccc"
    Then the response status code is 404
    And the "error" is "short url 'aaabbbccc' not found"