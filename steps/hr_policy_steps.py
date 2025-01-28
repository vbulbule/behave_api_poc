import requests
from behave import given, when, then
import json
from jsonschema import validate

BASE_URL = "https://api.hr-policy.example.com"  # Replace with the actual API URL


@given("the API endpoint is available")
def step_api_endpoint_is_available(context):
    context.endpoint = f"{BASE_URL}/query"
    response = requests.get(context.endpoint)
    assert response.status_code == 200, "API endpoint is not available"


@when('the user sends a query "{query}"')
def step_user_sends_query(context, query):
    context.query = query
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, data=json.dumps(payload), headers=headers)


@then('the response should contain "{expected_text}"')
def step_response_should_contain(context, expected_text):
    response_data = context.response.json()
    assert expected_text in response_data.get("message",
                                              ""), f'Expected text "{expected_text}" not found in the response'


@then("the response code should be {status_code:d}")
def step_response_code_should_be(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected status code {status_code}, but got {context.response.status_code}"
    )


@when("the user sends an invalid query {invalid_query}")
def step_user_sends_invalid_query(context, invalid_query):
    payload = {"query": invalid_query}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, data=json.dumps(payload), headers=headers)


@when("the user sends a malformed request")
def step_user_sends_malformed_request(context):
    payload = {"invalid_key": "invalid_value"}  # Malformed payload
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, data=json.dumps(payload), headers=headers)


@then("the response should contain an appropriate error message")
def step_response_should_contain_error_message(context):
    response_data = context.response.json()
    assert "error" in response_data, "Error message not found in the response"


@then('the response in Thai should match "{thai_response}"')
def step_response_in_thai_should_match(context, thai_response):
    response_data = context.response.json()
    assert response_data.get("thai_response") == thai_response, (
        f'Expected Thai response "{thai_response}", but got "{response_data.get("thai_response")}"'
    )


@then('the response in English should match "{english_response}"')
def step_response_in_english_should_match(context, english_response):
    response_data = context.response.json()
    assert response_data.get("english_response") == english_response, (
        f'Expected English response "{english_response}", but got "{response_data.get("english_response")}"'
    )


@then("the response time should be less than {time_limit:d} seconds")
def step_response_time_should_be_within_limit(context, time_limit):
    response_time = context.response.elapsed.total_seconds()
    assert response_time < time_limit, f"Response time {response_time} exceeded {time_limit} seconds"


@given("the API endpoint requires authentication")
def step_api_requires_authentication(context):
    context.endpoint = f"{BASE_URL}/query"


@when('the user sends a query "{query}"')
def step_user_sends_query(context, query):
    context.query = query
    payload = {"query": query}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {VALID_API_KEY}"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends a query with special characters")
def step_user_sends_special_characters_query(context):
    payload = {"query": "Flexible benefits @#$%^&*"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {VALID_API_KEY}"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when('the user sends an empty query "{query}"')
def step_user_sends_empty_query(context, query):
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends multiple queries within a short time")
def step_user_sends_multiple_queries(context):
    payload = {"query": "Flexible benefits คืออะไร"}
    headers = {"Content-Type": "application/json"}
    for _ in range(20):  # Simulate multiple requests
        context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends a query with unsupported language")
def step_user_sends_unsupported_language(context):
    payload = {"query": "¿Cuáles son los beneficios flexibles?"}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@then("the response should match the expected schema")
def step_response_matches_schema(context):
    response_data = context.response.json()
    expected_schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "thai_response": {"type": "string"},
            "english_response": {"type": "string"},
        },
        "required": ["message", "thai_response", "english_response"],
    }
    validate(instance=response_data, schema=expected_schema)


@then("the response should include CORS headers")
def step_response_includes_cors_headers(context):
    headers = context.response.headers
    assert "Access-Control-Allow-Origin" in headers, "CORS headers not found"
    assert headers["Access-Control-Allow-Origin"] == "*", "CORS header value is incorrect"


@when("the user sends a query with a payload larger than 1 MB")
def step_large_payload(context):
    large_query = "a" * 1024 * 1024  # Generate a 1 MB string
    payload = {"query": large_query}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends 10 concurrent queries")
def step_concurrent_queries(context):
    import threading

    def send_request():
        payload = {"query": "Flexible benefits คืออะไร"}
        headers = {"Content-Type": "application/json"}
        context.response = requests.post(context.endpoint, json=payload, headers=headers)

    threads = [threading.Thread(target=send_request) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@given("the upstream service is down")
def step_upstream_service_down(context):
    context.endpoint = f"{BASE_URL}/query"
    # Simulate upstream service failure by mocking the response
    context.response = requests.Response()
    context.response.status_code = 502
    context.response._content = b'{"message": "Bad gateway"}'


@when('the user sends a query with mixed languages "{query}"')
def step_query_mixed_languages(context, query):
    payload = {"query": query}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends a request without a valid API key")
def step_request_without_api_key(context):
    payload = {"query": "Flexible benefits คืออะไร"}
    headers = {"Content-Type": "application/json"}  # No Authorization header
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends a request with insufficient permissions")
def step_request_insufficient_permissions(context):
    payload = {"query": "Flexible benefits คืออะไร"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer invalid_role_key"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@when("the user sends a query with an SQL injection")
def step_sql_injection_query(context):
    payload = {"query": "'; DROP TABLE users;--"}
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(context.endpoint, json=payload, headers=headers)


@then("all responses should return status code 200")
def step_verify_all_responses_status_code(context):
    # Assuming `context.response` is a list of responses for concurrent requests
    assert all(response.status_code == 200 for response in context.responses), "Not all responses returned 200"


@then("all responses should be accurate")
def step_verify_all_responses_accuracy(context):
    # Assuming `context.response` is a list of responses for concurrent requests
    for response in context.responses:
        assert "Flexible Benefits" in response.json().get("message", ""), "Response message is inaccurate"

@given("the API endpoint requires specific roles")
def step_api_requires_specific_roles(context):
    context.endpoint = f"{BASE_URL}/query"
    context.headers = {"Content-Type": "application/json", "Authorization": "Bearer insufficient_role_key"}  # Simulate invalid role

@given("the API endpoint is temporarily unavailable")
def step_api_temporarily_unavailable(context):
    # Mock or simulate a 503 Service Unavailable response
    context.endpoint = f"{BASE_URL}/query"
    context.response = requests.Response()
    context.response.status_code = 503
    context.response._content = b'{"message": "Service is temporarily unavailable"}'

@given("a non-existent API endpoint")
def step_nonexistent_api_endpoint(context):
    context.endpoint = f"{BASE_URL}/nonexistent-endpoint"

@when('the user sends a request to "/nonexistent-endpoint"')
def step_user_sends_nonexistent_endpoint_request(context):
    context.response = requests.get(context.endpoint)