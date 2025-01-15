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


@given('I set the OpenAI API endpoint')
#@allure.step("Setting the OpenAI API endpoint")
def step_set_api_endpoint(context):
    context.api_url = API_URL
    context.headers = HEADERS
    allure.attach(str(context.api_url),name="Host URL", attachment_type=allure.attachment_type.TEXT)

# @allure.step("Sending a POST request to the OpenAI API")
# @when('I send a POST request to the OpenAI API')
# def step_send_post_request(context):
#     with open('payloads/request_payload.json', 'r') as file:
#         payload = json.load(file)
#     response = requests.post(context.api_url, headers=context.headers, json=payload)
#     context.response = response    

@given(u'I set the request payload as follows')
#@allure.step("Setting the request payload")
def step_set_request_payload(context):
    text = context.text.strip()
    context.payload = json.loads(text)
    allure.attach(json.dumps(context.payload, indent=2), name="Payload", attachment_type=allure.attachment_type.JSON)


@when('I send a POST request to the OpenAI API')
#@allure.step("Sending a POST request to the OpenAI API")
def step_send_post_request(context):
    response = requests.post(context.api_url, headers=context.headers, json=context.payload)
    context.response = response

    # Attach response details to the Allure report
    allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(json.dumps(response.json(), indent=2), name="Response Content", attachment_type=allure.attachment_type.JSON)

@then('the response status code should be {expected_status_code:d}')
#@allure.step("Verifying the response status code")
def step_verify_status_code(context, expected_status_code):
    actual_status_code = context.response.status_code
    assert actual_status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {actual_status_code}"
    )
    allure.attach(f"Expected: {expected_status_code}\nActual: {actual_status_code}", name="Status Code Verification", attachment_type=allure.attachment_type.TEXT)

#@allure.step("Verifying the content in the response")
@then('the response should contain the text "{expected_text}"')
def step_verify_response_content(context,expected_text):
    response_json = context.response.json()
    response_texts = [message['message']['content'] for message in response_json.get('choices', [])]
    assert any(expected_text in text for text in response_texts), f"Response does not contain expected text: {expected_text}"
    allure.attach(f"Expected Text: {expected_text}\nResponse Texts: {response_texts}", name="Content Verification", attachment_type=allure.attachment_type.TEXT)
