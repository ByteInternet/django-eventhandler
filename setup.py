from setuptools import setup

setup(
    name='django-eventhandler',
    version='',
    packages=['eventhandler'],
    url='https://github.com/ByteInternet/django-eventhandler',
    license='3-clause BSD',
    author='Gertjan Oude Lohuis',
    author_email='gertjan@byte.nl',
    description='RabbitMQ event handler as a Django module',
    install_requires=['Django', 'python-events']
)
