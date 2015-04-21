from setuptools import setup

setup(
    name="ordered-set",
    version = '1.3.1',
    maintainer='Luminoso Technologies, Inc.',
    maintainer_email='rob@luminoso.com',
    license = "MIT-LICENSE",
    url = 'http://github.com/LuminosoInsight/ordered-set',
    platforms = ["any"],
    description = "A MutableSet that remembers its order, so that every entry has an index.",
    py_modules=['ordered_set'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
