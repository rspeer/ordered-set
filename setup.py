# This is a wrapper for environments that require a `setup.py`-based installation.
# This is not the primary way of installing ordered-set.
#
# The primary setup is in pyproject.toml. You can install ordered-set as a
# dependency using `poetry` or `pip`.

from setuptools import setup

packages = ['ordered_set']

setup_kwargs = {
    'name': 'ordered-set',
    'version': '4.1.0',
    'description': 'A set that remembers its order, and allows looking up its items by their index in that order.',
    'author': 'Elia Robyn Lake',
    'author_email': 'elial@ec.ai',
    'url': 'https://github.com/rspeer/ordered-set',
    'packages': packages,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

