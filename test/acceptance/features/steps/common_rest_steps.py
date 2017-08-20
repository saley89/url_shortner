import json

import requests
from behave import given, when, then
from nose.tools import assert_equal, assert_in, assert_true
from validators import url


@given(u'the request body is invalid JSON')
def request_body_is_invalid_json(context):
    context.request_body = '{'


@given(u'the request body is not supplied')
def request_body_is_not_supplied(context):
    context.request_body = None


@given(u'the request body is empty JSON')
def request_body_is_empty_json(context):
    context.request_body = {}


@given(u'the url is "{url}"')
def the_url_is(context, url):
    context.request_body = {'url': url}


@when(u'I post "{service}"')
def execute_post_rest_call_to(context, service):
    if isinstance(context.request_body, dict):
        context.response = requests.post("http://localhost:8000/{}".format(service), json=context.request_body)
    else:
        context.response = requests.post("http://localhost:8000/{}".format(service), data=context.request_body)


@when(u'I get "{service}"')
def execute_get_rest_call_to(context, service):
    context.response = requests.get("http://localhost:8000/{}".format(service), allow_redirects=False)


@then(u'the response status code is {code}')
def response_status_code_is(context, code):
    print(context.response.text)
    assert_equal(int(code), context.response.status_code)


@then(u'the response body contains "{key}"')
def response_body_contains(context, key):
    assert_in(key, json.loads(context.response.text))


@then(u'the "{key}" returned is a valid url')
def key_returned_is_valid_url(context, key):
    response = json.loads(context.response.text)
    assert_true(url((response[key])))


@then(u'the "{key}" is "{value}"')
def actual_json_value_equals_expected_value(context, key, value):
    response = json.loads(context.response.text)
    assert_equal(response[key], value)
