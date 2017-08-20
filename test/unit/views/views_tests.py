import json
import unittest
from unittest.mock import patch

from url_shortner import app


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.service_patcher = patch('url_shortner.views.shortner_views.ShortenService')
        self.mock_shortner_service = self.service_patcher.start().return_value
        self.mock_shortner_service.validate.return_value = True, None

    def tearDown(self):
        self.service_patcher.stop()

    def test_shorten_url_view_returns_201_if_created_successfully(self):
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual(201, result.status_code)

    def test_shorten_url_view_returns_json_body_with_url_if_successful(self):
        self.mock_shortner_service.store_url.return_value = 'id12345'
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual({'shortened_url': 'http://localhost:8000/id12345'}, json.loads(result.data))

    def test_shorten_url_view_returns_400_if_validation_returns_errors(self):
        self.mock_shortner_service.validate.return_value = False, 'something was wrong'
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual(400, result.status_code)

    def test_shorten_url_view_returns_error_json_if_validation_fails(self):
        self.mock_shortner_service.validate.return_value = False, 'something was wrong'
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual({'error': 'something was wrong'}, json.loads(result.data))

    def test_shorten_url_view_returns_500_if_unexpected_error(self):
        self.mock_shortner_service.validate.side_effect = TypeError
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual(500, result.status_code)

    def test_shorten_url_view_returns_error_json_if_unexected_error(self):
        self.mock_shortner_service.validate.side_effect = TypeError
        result = self.app.post('/shorten_url', data=json.dumps({'url': 'http://www.google.com'}))
        self.assertEqual({'error': 'Unexpected exception occurred: '}, json.loads(result.data))

    def test_redirect_url_view_returns_redirect_status(self):
        self.mock_shortner_service.retrieve_url.return_value = "http://www.google.com"
        result = self.app.get('/id12345')
        self.assertEqual(302, result.status_code)

    def test_redirect_url_view_redirects_to_retrieved_url(self):
        self.mock_shortner_service.retrieve_url.return_value = "http://www.google.com"
        result = self.app.get('/id12345')
        self.assertEqual('http://www.google.com', result.headers['Location'])

    def test_redirect_url_view_returns_not_found_status_if_not_in_db(self):
        self.mock_shortner_service.retrieve_url.return_value = None
        result = self.app.get('/id12345')
        self.assertEqual(404, result.status_code)

    def test_redirect_url_view_returns_not_found_error_if_not_in_db(self):
        self.mock_shortner_service.retrieve_url.return_value = None
        result = self.app.get('/id12345')
        self.assertEqual({"error": "short url 'id12345' not found"}, json.loads(result.data))