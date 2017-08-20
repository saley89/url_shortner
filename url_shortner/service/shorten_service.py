import base64
import hashlib
import json
import logging

from validators import url

from url_shortner.data.url_repository import UrlRepository

LOG = logging.getLogger(__name__)


class ShortenService(object):
    def __init__(self):
        self.repository = UrlRepository()

    def validate(self, request):
        checks = [self._is_valid_json, self._has_mandatory_data, self._is_valid_url]
        for check in checks:
            valid, msg = check(request)
            if not valid:
                return False, msg
        return True, None

    @staticmethod
    def _is_valid_json(request):
        try:
            json.loads(request.data or '{}')
            return True, None
        except Exception as e:
            LOG.error("Exception occurred validating request, %s", str(e))
        return False, "Invalid JSON supplied"

    @staticmethod
    def _has_mandatory_data(request):
        data = json.loads(request.data or '{}')
        try:
            data['url']
            return True, ''
        except KeyError:
            return False, 'Missing mandatory data: "url"'

    @staticmethod
    def _is_valid_url(request):
        data = json.loads(request.data or '{}')
        valid = url(data.get('url'))
        return valid, 'Invalid url supplied'

    def store_url(self, url):
        hash_object = hashlib.md5(url.encode())
        identifier = base64.urlsafe_b64encode(hash_object.digest()).decode('UTF-8')
        self.repository.store(identifier, url)
        return identifier

    def retrieve_url(self, identifier):
        return self.repository.get(identifier)
