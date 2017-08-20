import unittest
from unittest.mock import patch

from url_shortner.exceptions import DatabaseErrorException
from redis import RedisError

from url_shortner.data.url_repository import UrlRepository


class TestUrlRepository(unittest.TestCase):

    def setUp(self):
        self.redis_patcher = patch('url_shortner.data.url_repository.get_cached_redis_store')
        self.mock_redis = self.redis_patcher.start().return_value
        self.repo = UrlRepository()

    def tearDown(self):
        self.mock_redis.stop()

    def test_store_inserts_url_into_database(self):
        self.repo.store('some-id', 'http://some-url.com')
        self.mock_redis.set.assert_called_once_with('some-id', 'http://some-url.com')

    def test_store_raises_exception_if_database_connection_fails(self):
        self.mock_redis.set.side_effect = RedisError
        self.assertRaises(DatabaseErrorException, self.repo.store, 'some-id', 'http://some-url.com')

    def test_get_returns_url_stored_in_database(self):
        self.mock_redis.get.return_value = b'http://some-url.com'
        actual = self.repo.get('some-id')
        self.mock_redis.get.assert_called_once_with('some-id')
        self.assertEqual('http://some-url.com', actual)

    def test_get_returns_none_if_url_not_in_database(self):
        self.mock_redis.get.return_value = None
        actual = self.repo.get('some-id')
        self.mock_redis.get.assert_called_once_with('some-id')
        self.assertIsNone(actual)

    def test_get_raises_exception_if_database_connection_fails(self):
        self.mock_redis.get.side_effect = RedisError
        self.assertRaises(DatabaseErrorException, self.repo.get, 'some-id')