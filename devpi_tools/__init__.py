import requests

class DevpiApiError(RuntimeError):
    """ Error from devpi web interface """

class DevpiObject(object):
    """ Client response object """
    path = None
    _client = None

    def get_json(self, path):
        return self._client.get_json(path)

    def __str__(self):
        return self.path

class DevpiIndex(DevpiObject):
    """ Represents a remote devpi index """

    def __init__(self, client, path, config):
        self._client = client
        self.path = path
        self.config = config
        _, self.user, self.name = path.split('/')

    def project(self, name):
        return DevpiProject(self._client, '%s/%s' % (self.path, name))

    def projects(self):
        return list(self.iter_projects())

    def iter_projects(self):
        res = self.get_json(self.path)
        for p in res['projects']:
            yield DevpiProject(self._client, '%s/%s' % (self.path, p))

    def __repr__(self):
        return '<devpitools.Index %s>' % self.path

class DevpiProject(DevpiObject):
    """ Represents a remote devpi project """

    def __init__(self, client, path):
        self._client = client
        self.path = path

    def version(self, version):
        return self.get_json('%s/%s' % (self.path, version))

    def versions(self):
        return self.get_json(self.path)

    def __repr__(self):
        return '<devpitools.Project %s>' % self.path

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
