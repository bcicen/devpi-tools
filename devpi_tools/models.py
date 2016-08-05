from datetime import datetime

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
        path = '%s/%s' % (self.path, version)
        return DevpiVersion(path, self.get_json(path))

    def versions(self):
        return list(self.iter_versions())

    def iter_versions(self):
        for vmeta in self.get_json(self.path).values():
            path = '%s/%s' % (self.path, vmeta['version'])
            yield DevpiVersion(path, vmeta)

    def __repr__(self):
        return '<devpitools.Project %s>' % self.path

class DevpiVersion(DevpiObject):
    """ Represents a dist of a remote devpi project """

    def __init__(self, path, meta):
        self.path = path
        self.links = self._read_links(meta.pop('+links'))
        for k,v in meta.items():
            self.__setattr__(k,v)

    @staticmethod
    def _read_links(links):
        return [ DevpiLink(self.path, l) for l in links ]

    def __repr__(self):
        return '<devpitools.Version %s>' % self.path

class DevpiLink(DevpiObject):
    """ Represents links associated with a remote devpi project """

    def __init__(self, path, meta):
        self.path = path
        self.log = self._read_log(meta.pop('log'))
        for k,v in meta.items():
            self.__setattr__(k,v)

    @staticmethod
    def _read_log(log):
        """ read log timestamp into datetime obj """
        for l in log:
            year, month, date, hour, minute, second = l['when']
            l['when'] = datetime(year, month, date, hour, minute, second)
        return log

    def __repr__(self):
        return '<devpitools.Link %s>' % self.path
