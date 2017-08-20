import logging
from redis import RedisError

from url_shortner.exceptions import DatabaseErrorException
from url_shortner.data.redis_utils import get_cached_redis_store

LOG = logging.getLogger(__name__)


class UrlRepository(object):

    def __init__(self):
        self.redis = get_cached_redis_store()

    def store(self, identifier, url):
        return self._execute(self.redis.set, identifier, url)

    def get(self, identifier):
        value = self._execute(self.redis.get, identifier)
        if value:
            return value.decode('UTF-8')

    @staticmethod
    def _execute(method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except RedisError as e:
            LOG.error('Error communicating with database: %s', e)
            raise DatabaseErrorException("Error communicating with database: {}".format(str(e)))
