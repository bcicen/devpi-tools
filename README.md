# devpi-tools
Small Python library for interacting with devpi servers via web API

## Installing 

```python
pip install devpi-tools
```

## Usage

```python
from devpi_tools.devpi_connector import DevpiClient

client = DevpiClient('http://127.0.0.1:3141')

client.indexes() # list all indexes
index = client.index('/root/pypi') # fetch a single index

index.projects() # list all projects
project = index.project('devpi-tools') # fetch a single project/package by name

project.versions() # list of uploaded versions
project.version('1.0.1') # fetch details on a specific version
```


Another example, finding the latest version of a specific package, in a specific devpi index:
```python
index = client.index('/root/pypi')
v = index.project('requests').latest_version()
print('version: %s' % v.version)
print('uploaded: %s' % v.uploaded)
```

