Feature: Verify OpenAI API Responses

  Scenario: Verify status code of OpenAI API response
    Given I set the OpenAI API endpoint
    And I set the request payload as follows:
      """
      {
    "messages": [
     {
      "role": "system",
      "content": "you are a helpful assistant that answers questions professonally"
     },
     {
      "role": "user",
      "content": "What is the capital of India?"
     }
    ]
   }
      """
    When I send a POST request to the OpenAI API
    Then the response status code should be 200

  Scenario: Verify content in OpenAI API response
    Given I set the OpenAI API endpoint
    And I set the request payload as follows:
      """
      {
    "messages": [
     {
      "role": "system",
      "content": "you are a helpful assistant that answers questions professonally"
     },
     {
      "role": "user",
      "content": "list all the java keywords"
     }
    ]
   }
      """
    When I send a POST request to the OpenAI API
    Then the response status code should be 200
    Then the response should contain the text "default"
