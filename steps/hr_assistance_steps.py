import requests
from behave import given, when, then
import json
import os
from dotenv import load_dotenv
import allure

# Load environment variables from .env file
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

@given('I set the HR Assistance')
def step_set_api_endpoint(context):
    context.api_url_hr = API_URL
    context.headers_hr = HEADERS
    allure.attach(str(context.api_url_hr),name="HR Assistance", attachment_type=allure.attachment_type.TEXT)

@given(u'I ask Question as follows')
def step_set_hr_question_payload(context):
        text = context.text.strip()
        context.payload = json.loads(text)
        allure.attach(json.dumps(context.payload, indent=2), name="Question",
                      attachment_type=allure.attachment_type.JSON)


@then('the response status code should be "{expected_status_code}"')
def step_verify_status_code(context, expected_status_code):
    """
    Verifies that the response status code matches the expected status code.
    """
    actual_status_code = context.response.json().get("data", {}).get("status", {}).get("code")
    assert actual_status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {actual_status_code}."
    )
    allure.attach(
        f"Expected: {expected_status_code}\nActual: {actual_status_code}",
        name="Status Code Verification",
        attachment_type=allure.attachment_type.TEXT
    )

@when('I send a POST request to the HR Assistance API')
def step_send_post_request_hr(context):
    response = requests.post(context.api_url_hr, headers=context.headers_hr, json=context.payload)
    context.response = response

    # Attach response details to the Allure report
    allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(json.dumps(response.json(), indent=2), name="Response Content", attachment_type=allure.attachment_type.JSON)

@then('the agent response should contain the text "{expected_text}"')
def step_verify_agent_response(context, expected_text):
    """
    Verifies that the agent's response contains the expected text.
    """
    agent_response_content = context.response.json().get("data", {}).get("agent_response", {}).get("content", "")
    assert expected_text in agent_response_content, (
        f"Expected text '{expected_text}' not found in agent response: {agent_response_content}."
    )
    allure.attach(
        f"Expected Text: {expected_text}\nAgent Response Content: {agent_response_content}",
        name="Agent Response Verification",
        attachment_type=allure.attachment_type.TEXT
    )




