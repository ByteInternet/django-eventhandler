from setuptools import setup

setup(
    name='django-eventhandler',
    version='0.1',
    provides=['eventhandler'],
    packages=['eventhandler'],
    url='https://github.com/ByteInternet/django-eventhandler',
    license='3-clause BSD',
    author='Gertjan Oude Lohuis',
    author_email='gertjan@byte.nl',
    description='RabbitMQ event handler as a Django module',
    install_requires=['Django>=1.6', 'python-events==0.1'],
    dependency_links=['https://github.com/ByteInternet/python-events/tarball/master#egg=python-events-0.1']
)
