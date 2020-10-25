from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with open(path.join(pwd, 'README.md'), encoding='utf-8') as of:
    long_description = of.read()

setup(
  name='devpi-tools',
  version='0.5.3',
  packages=['devpi_tools'],
  description='library for interacting with devpi servers via web API',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Bradley Cicenas',
  author_email='bradley@vektor.nyc',
  url='https://github.com/bcicen/devpi-tools',
  install_requires=['requests>=2.9.1'],
  license='http://opensource.org/licenses/MIT',
  include_package_data=True,
  classifiers=[
      'Natural Language :: English',
      'Programming Language :: Python',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
      'License :: OSI Approved :: MIT License ',
  ],
  keywords='devpi pypi packaging devops',
)
