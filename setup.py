""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='zopper.ws',
    version=0.1,
    description='Components to fulfill zopper Web Services requirements.',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords="web services",
    author='Safiulla',
    author_email='safiulla.sk@gmail.com',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cornice',
        'waitress',
        'SQLAlchemy==0.7.6'
        ],
    entry_points = """\
    [paste.app_factory]
    main = zopper.ws:main
    """,
    paster_plugins=['pyramid'],
)
