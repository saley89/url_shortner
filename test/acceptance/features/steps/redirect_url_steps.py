import requests
from behave import given, then
from nose.tools import assert_equal


@given(u'stored url is "{url}"')
def stored_url_is(context, url):
    response = requests.post("http://localhost:8000/shorten_url", json={'url': url})
    assert_equal(201, response.status_code)


@then(u'the redirection is to "{url}"')
def redirection_is_to(context, url):
    assert_equal(context.response.headers['Location'], url)
