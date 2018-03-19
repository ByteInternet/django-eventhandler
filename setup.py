from setuptools import setup, find_packages

setup(
    name='django-eventhandler',
    version='0.5.1',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/ByteInternet/django-eventhandler',
    author='Byte B.V.',
    author_email='tech@byte.nl',
    license='3-clause BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Communications',
        'Topic :: Internet',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='amqp django rabbitmq events eventhandler',
    description='RabbitMQ event handler as a Django module',
    install_requires=['Django>=1.6', 'amqpconsumer==1.5'],
)
