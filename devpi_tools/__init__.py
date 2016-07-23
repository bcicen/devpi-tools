import time
import requests

class DevpiObject(object):
    """ Client response object """
    _client = None
    def get_json(self, path):
        return self._client.get_json(path)

class DevpiIndex(DevpiObject):
    """ Represents a remote devpi index """

    def __init__(self, client, path, config):
        self._client = client
        self.path = path
        self.config = config
        _, self.user, self.name = path.split('/')

    @property
    def projects(self):
        res = self.get_json(self.path)
        for p in res['result']['projects']:
            yield DevpiProject(self._client, '%s/%s' % (self.path, p))

    def __repr__(self):
        return '<devpitools.Index %s>' % self.path

    def __str__(self):
        return '%s/%s' % (self.user, self.name)

class DevpiProject(DevpiObject):
    """ Represents a remote devpi project """

    def __init__(self, client, path):
        self._client = client
        self.path = path

    @property
    def versions(self):
        return self.get_json(self.path)['result']

    def __repr__(self):
        return '<devpitools.Project %s>' % self.path

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

    def get_index(self, path):
        return DevpiIndex(self, path, {})

    def indexes(self):
        res = self.get_json('/')['result']
        for k,v in res.items():
            user = k
            for name, config in v['indexes'].items():
                path = '/%s/%s' % (user, name)
                yield DevpiIndex(self, path, config)
