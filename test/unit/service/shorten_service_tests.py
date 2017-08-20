import unittest
from unittest.mock import patch, Mock

from flask import Request

from url_shortner.exceptions import DatabaseErrorException
from url_shortner.service.shorten_service import ShortenService


class TestShortenService(unittest.TestCase):

    def setUp(self):
        self.mock_repo_patcher = patch('url_shortner.service.shorten_service.UrlRepository')
        self.mock_repository = self.mock_repo_patcher.start().return_value
        self.service = ShortenService()

    def tearDown(self):
        self.mock_repo_patcher.stop()

    def test_validate_returns_error_if_url_supplied_not_valid(self):
        request = Mock(spec=Request)
        request.data = b'{"url": "not valid"}'
        is_valid, reason = self.service.validate(request)
        self.assertFalse(is_valid)
        self.assertEqual(reason, 'Invalid url supplied')

    def test_validate_returns_error_if_url_supplied_empty(self):
        request = Mock(spec=Request)
        request.data = b'{"url": ""}'
        is_valid, reason = self.service.validate(request)
        self.assertFalse(is_valid)
        self.assertEqual(reason, 'Invalid url supplied')

    def test_validate_returns_error_if_url_is_missing_in_request(self):
        request = Mock(spec=Request)
        request.data = b'{}'
        is_valid, reason = self.service.validate(request)
        self.assertFalse(is_valid)
        self.assertEqual(reason, 'Missing mandatory data: "url"')

    def test_validate_returns_error_if_request_body_not_supplied(self):
        request = Mock(spec=Request)
        request.data = None
        is_valid, reason = self.service.validate(request)
        self.assertFalse(is_valid)
        self.assertEqual(reason, 'Missing mandatory data: "url"')

    def test_validate_returns_error_if_json_invalid(self):
        request = Mock(spec=Request)
        request.data = b'{'
        is_valid, reason = self.service.validate(request)
        self.assertFalse(is_valid)
        self.assertEqual(reason, 'Invalid JSON supplied')

    def test_store_url_returns_identifier_for_url(self):
        identifier = self.service.store_url("http://some-url.com")
        self.assertEqual('P4SI4cAJ_dSNiE5mM7Umnw==', identifier)

    def test_store_url_stores_encoded_url_in_repository(self):
        self.service.store_url("http://some-url.com")
        self.mock_repository.store.assert_called_once_with('P4SI4cAJ_dSNiE5mM7Umnw==', 'http://some-url.com')

    def test_store_url_raises_exceptions_from_repository(self):
        self.mock_repository.store.side_effect = DatabaseErrorException()
        self.assertRaises(DatabaseErrorException, self.service.store_url, "http://some-url.com")

    def test_retrieve_url_returns_url_for_given_identifier(self):
        self.mock_repository.get.return_value = 'http://some-url.com'
        url = self.service.retrieve_url("some-id")
        self.assertEqual('http://some-url.com', url)

    def test_retrieve_url_raises_exceptions_from_repository(self):
        self.mock_repository.get.side_effect = DatabaseErrorException()
        self.assertRaises(DatabaseErrorException, self.service.retrieve_url, "http://some-url.com")