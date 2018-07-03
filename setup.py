from setuptools import setup

DESCRIPTION = open('README.md').read()


setup(
    name="ordered-set",
    version = '3.0.1',
    maintainer='Luminoso Technologies, Inc.',
    maintainer_email='rspeer@luminoso.com',
    license = "MIT-LICENSE",
    url = 'http://github.com/LuminosoInsight/ordered-set',
    platforms = ["any"],
    description = "A MutableSet that remembers its order, so that every entry has an index.",
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    py_modules=['ordered_set'],
    package_data={'': ['MIT-LICENSE']},
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=2.7',
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
