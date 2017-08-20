Feature:
  User provides a url to the API to be shortened

  Scenario: User supplies a valid url - return shortened url
    Given the url is "http://www.google.com"
    When I post "shorten_url"
    Then the response status code is 201
    And the response body contains "shortened_url"
    And the "shortened_url" is "http://localhost:8000/7WRqMzTKiR_TRn2xMTchQA=="

  Scenario: User supplies an invalid url
    Given the url is "not valid url format"
    When I post "shorten_url"
    Then the response status code is 400
    And the response body contains "error"
    And the "error" is "Invalid url supplied"

  Scenario: User supplies empty url value
    Given the url is " "
    When I post "shorten_url"
    Then the response status code is 400
    And the response body contains "error"
    And the "error" is "Invalid url supplied"

  Scenario: User supplies valid JSON missing url key
    Given the request body is empty JSON
    When I post "shorten_url"
    Then the response status code is 400
    And the response body contains "error"
    And the "error" is "Missing mandatory data: "url""

  Scenario: User supplies invalid JSON
    Given the request body is invalid JSON
    When I post "shorten_url"
    Then the response status code is 400
    And the response body contains "error"
    And the "error" is "Invalid JSON supplied"

  Scenario: User supplies no body
    Given the request body is not supplied
    When I post "shorten_url"
    Then the response status code is 400
    And the response body contains "error"
    And the "error" is "Missing mandatory data: "url""