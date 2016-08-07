from setuptools import setup

setup(name='devpi-tools',
      version='0.3',
      packages=['devpi_tools'],
      description='library for interacting with devpi servers via web API',
      author='Bradley Cicenas',
      author_email='bradley@vektor.nyc',
      url='https://github.com/bcicen/devpi-tools',
      install_requires=['requests>=2.9.1'],
      license='http://opensource.org/licenses/MIT',
      classifiers=(
          'Natural Language :: English',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License ',
      ),
      keywords='devpi pypi packaging devops',
)
