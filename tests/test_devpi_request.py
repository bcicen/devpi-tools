from devpi_tools.devpi_request import DevpiClient
import json


def mock_get_json_index(self, path, method='GET', **params):
    return {
        "root": {
          "indexes": {
            "pypi": {
              "type": "mirror",
              "volatile": False,
              "title": "PyPI",
              "mirror_url": "https://pypi.org/simple/",
              "mirror_web_url_fmt": "https://pypi.org/project/{name}/"
            },
          },
          "username": "root"
        }
    }


def mock_get_projects_json(self, path, method='GET', **params):
    return {
        "type": "stage",
        "volatile": True,
        "acl_upload": [
          "root",
        ],
        "acl_toxresult_upload": [
          ":ANONYMOUS:"
        ],
        "bases": [],
        "mirror_whitelist": [],
        "pypi_whitelist": [],
        "projects": [
          "devpi-tools"
        ]
    }


def mock_get_project_json(self, path, method='GET', **params):
    json_file_path = './files/project.json'
    with open(json_file_path) as f:
        json_dict = json.load(f)
    return json_dict


def mock_get_version_json(self, path, method='GET', **params):
    json_file_path = './files/version.json'
    with open(json_file_path, 'r') as f:
        json_dict = json.load(f)
    return json_dict


def test_devpi_request_indexes(monkeypatch):
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_json_index)
    client = DevpiClient('http://127.0.0.1:3141')
    list_indexes = client.indexes()
    assert len(list_indexes) == 1
    assert list_indexes[0].name == "pypi"
    index = client.index('/root/pypi')
    assert index.user == "root"


def test_devpi_request_projects(monkeypatch):
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_json_index)
    client = DevpiClient('http://127.0.0.1:3141')
    index = client.index('/root/pypi')
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_projects_json)
    list_projects = index.projects()
    assert len(list_projects) == 1
    assert list_projects[0].path == "/root/pypi/devpi-tools"

    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_project_json)
    project = index.project('devpi-tools')
    assert project.path == "/root/pypi/devpi-tools"


def test_devpi_request_version(monkeypatch):
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_json_index)
    client = DevpiClient('http://127.0.0.1:3141')

    index = client.index('/root/pypi')
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_project_json)
    project = index.project('devpi-tools')
    monkeypatch.setattr(DevpiClient, 'get_json', mock_get_version_json)
    version = project.version('0.0.1')
    assert version.path == "/root/pypi/devpi-tools/0.0.1"
    assert version.version == "0.0.1"
    assert version.author == "Bradley Cicenas"
