import time
import requests

class DevpiResponse(object):
    """ Client response object """
    def __init__(self, client):
        self._client = client

class DevpiIndex(DevpiResponse):
    """ Represents a remote devpi index """
    user = None
    name = None
    config = None

    def _populate(self, user, name, config):
        self.user = user
        self.name = name
        self.config = config

    @property
    def projects(self):
        return self._client.get_json('/%s/%s' % (self.user, self.name))

    def __repr__(self):
        return '<DevpiIndex %s/%s>' % (self.user, self.name)

    def __str__(self):
        return '%s/%s' % (self.user, self.name)

class DevpiClient(requests.Session):
    """ A very small client for connecting to devpi web API """
    def __init__(self, base_url):
        super(DevpiClient, self).__init__()
        self.base_url = base_url

    def get_json(self, path, method='GET', **params):
        url = self.base_url + path
        headers = { 'Accept': 'application/json' }

        res = self.request(method, url, headers=headers)
        res.raise_for_status()
        return res.json()

    def indexes(self):
        res = self.get_json('/')['result']
        for k,v in res.items():
            user = k
            for name, config in v['indexes'].items():
                index = DevpiIndex(self)
                index.user = user
                index.name = name
                index.config = name
                yield index
