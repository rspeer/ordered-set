from setuptools import setup
import sys

setup(
    name="ordered-set",
    version = '1.0',
    maintainer='Luminoso, LLC',
    maintainer_email='dev@lumino.so',
    license = "MIT-LICENSE",
    url = 'http://github.com/LuminosoInsight/orderedset',
    platforms = ["any"],
    description = "A MutableSet that remembers its order, so that every entry has an index.",
    py_modules=['ordered_set'],
)
