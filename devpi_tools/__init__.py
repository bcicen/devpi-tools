import requests
from .models import DevpiIndex

class DevpiApiError(RuntimeError):
    """ Error from devpi web interface """

class DevpiClient(requests.Session):
    """ A very small client for connecting to devpi web API """
    def __init__(self, base_url):
        super(DevpiClient, self).__init__()
        self.base_url = base_url

    def get_json(self, path, method='GET', **params):
        url = self.base_url + path
        headers = { 'Accept': 'application/json' }

        res = self.request(method, url, headers=headers).json()
        if 'message' in res.keys():
            raise DevpiApiError(res['message'])

        return res['result']

    def index(self, path):
        for i in self.iter_indexes():
            if i.path == path:
                return i
        raise DevpiApiError('no such index: %s' % path)

    def indexes(self):
        return list(self.iter_indexes())

    def iter_indexes(self):
        for user, info in self.get_json('/').items():
            for name, config in info['indexes'].items():
                path = '/%s/%s' % (user, name)
                yield DevpiIndex(self, path, config)
