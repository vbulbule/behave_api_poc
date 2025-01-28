Feature: Verify HR Policy API responses
  As a QA Engineer
  I want to ensure that the HR Policy API responses are accurate
  So that users can rely on them for correct information

  Scenario Outline: Verify response content for valid queries
    Given the API endpoint is available
    When the user sends a query "<query>"
    Then the response should contain "<expected_text>"
    And the response code should be 200

    Examples:
      | query                                           | expected_text                                    |
      | Flexible benefits คืออะไร                       | Flexible Benefits means flexible health benefits |
      | พนักงานสามารถใช้ flexible benefits กับอะไรได้บ้าง | Flexible Benefits can be used to cover health   |

  Scenario: Verify response for invalid query
    Given the API endpoint is available
    When the user sends an invalid query "Invalid Query"
    Then the response should contain "I don't have information"
    And the response code should be 404

  Scenario: Verify response code for malformed request
    Given the API endpoint is available
    When the user sends a malformed request
    Then the response code should be 400
    And the response should contain an appropriate error message

  Scenario Outline: Validate Thai and English translations in response
    Given the API endpoint is available
    When the user sends a query "<query>"
    Then the response in Thai should match "<thai_response>"
    And the response in English should match "<english_response>"
    And the response code should be 200

    Examples:
      | query                                           | thai_response                                     | english_response                                   |
      | Flexible benefits คืออะไร                       | สวัสดิการแบบยืดหยุ่น (Flexible Benefits) หมายถึง... | Flexible Benefits means flexible health benefits |
      | พนักงานสามารถใช้ flexible benefits กับอะไรได้บ้าง | สวัสดิการแบบยืดหยุ่น...                      | Flexible Benefits can be used to cover health   |

  Scenario: Verify response time for API queries
    Given the API endpoint is available
    When the user sends a query "Flexible benefits คืออะไร"
    Then the response time should be less than 2 seconds

    Scenario: Verify response when the query contains special characters
    Given the API endpoint is available
    When the user sends a query "Flexible benefits @#$%^&*"
    Then the response code should be 400
    And the response should contain an appropriate error message

  Scenario: Verify response when the query is empty
    Given the API endpoint is available
    When the user sends an empty query " "
    Then the response code should be 400
    And the response should contain "Query parameter cannot be empty"

  Scenario: Verify response for unsupported language input
    Given the API endpoint is available
    When the user sends a query "¿Cuáles son los beneficios flexibles?"
    Then the response code should be 400
    And the response should contain "Unsupported language"

  Scenario: Validate case-insensitive query handling
    Given the API endpoint is available
    When the user sends a query "FLEXIBLE BENEFITS คืออะไร"
    Then the response should contain "Flexible Benefits means flexible health benefits"
    And the response code should be 200

  Scenario: Verify rate limiting for API queries
    Given the API endpoint is available
    When the user sends multiple queries within a short time
    Then the response code should be 429
    And the response should contain "Rate limit exceeded"

  Scenario: Verify response for SQL injection in the query
    Given the API endpoint is available
    When the user sends a query "'; DROP TABLE users;--"
    Then the response code should be 400
    And the response should contain "Invalid query input"

  Scenario: Validate response schema for a valid query
    Given the API endpoint is available
    When the user sends a query "Flexible benefits คืออะไร"
    Then the response should match the expected schema
    And the response code should be 200

  Scenario: Validate API authentication failure
    Given the API endpoint requires authentication
    When the user sends a request without a valid API key
    Then the response code should be 401
    And the response should contain "Authentication required"

  Scenario: Validate API authorization failure
    Given the API endpoint requires specific roles
    When the user sends a request with insufficient permissions
    Then the response code should be 403
    And the response should contain "Access denied"

  Scenario: Validate response when the server is under maintenance
    Given the API endpoint is temporarily unavailable
    When the user sends a query "Flexible benefits คืออะไร"
    Then the response code should be 503
    And the response should contain "Service is temporarily unavailable"

  Scenario: Verify response for non-existent endpoint
    Given a non-existent API endpoint
    When the user sends a request to "/nonexistent-endpoint"
    Then the response code should be 404
    And the response should contain "Endpoint not found"

  Scenario: Verify large payload handling
    Given the API endpoint is available
    When the user sends a query with a payload larger than 1 MB
    Then the response code should be 413
    And the response should contain "Payload too large"

  Scenario: Validate CORS headers in API response
    Given the API endpoint is available
    When the user sends a query "Flexible benefits คืออะไร"
    Then the response should include CORS headers
    And the response code should be 200

  Scenario: Validate responses for multiple concurrent requests
    Given the API endpoint is available
    When the user sends 10 concurrent queries
    Then all responses should return status code 200
    And all responses should be accurate

  Scenario: Verify response for query with mixed languages
    Given the API endpoint is available
    When the user sends a query "Flexible benefits กับอะไรได้บ้าง?"
    Then the response should contain "Flexible Benefits can be used to cover health"
    And the response code should be 200

  Scenario: Validate API behavior when upstream service fails
    Given the upstream service is down
    When the user sends a query "Flexible benefits คืออะไร"
    Then the response code should be 502
    And the response should contain "Bad gateway"

