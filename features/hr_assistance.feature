Feature: Verify HR Assistance Responses

  Scenario: Verify status code of HR Assistance
    Given I set the HR Assistance
    And I ask Question as follows
      """
      {
          "messages": [
              {
                  "role": "system",
                  "content": "you are a helpful assistant that talks like a pirate"
              },
              {
                  "role": "user",
                  "content": "list all the keywords in java"
              }
          ]
      }
      """
    When I send a POST request to the HR Assistance API
    Then the response status code should be 200

  Scenario: Verify content in HR Assistance
    Given I set the HR Assistance
    And I ask Question as follows
      """
      {
          "messages": [
              {
                  "role": "system",
                  "content": "you are a helpful assistant that answers professionally"
              },
              {
                  "role": "user",
                  "content": "list all the keywords in java"
              }
          ]
      }
      """
    When I send a POST request to the HR Assistance API
    Then the response status code should be 200
    Then the agent response should contain the text "default"
