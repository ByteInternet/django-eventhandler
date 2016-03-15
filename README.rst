===================
django-eventhandler
===================
This is an event handler that handles messages from an AMQP server, installable as a Django application. You can bind

Installation and configuration
------------------------------
Install the application in your Django project. Add `'eventhandler'` to your `INSTALLED_APPS` setting. Then, add the
following two settings to your project settings file.
::

  LISTENER_URL = 'amqps://<user>:<pass>@<hostname>/<vhost>'
  LISTENER_QUEUE = 'my-application'

Optionally, you can also specify these three settings, to have an exchange declared.
::

  LISTENER_EXCHANGE = 'events'
  LISTENER_EXCHANGE_TYPE = 'topic'
  LISTENER_ROUTING_KEY = '#'

Running the event handler
-------------------------
Manually: `python manage.py event_listener`. To daemonize it, you can use something like `supervisor` to manage the
process.

Usage
-----
Events that are received from AMQP should be JSON messages. Each message should have a key named `type`, with a `str`
value. This value can be used in a decorator, to have the event handler execute a function when receiving an event.

Example:

.. code-block:: python

    from eventhandler import handles_event

    @handles_event('my_event')
    def do_something_clever(event):
        pass

Now each event with a `'type': 'my_event'` combo will be passed into this function. Of course it's possible to have
more than one handler for an event, or have one handler handle multiple events.

.. code-block:: python

    from eventhandler import handles_event

    @handles_event('my_other_event')
    @handles_event('my_event')
    def do_something_clever(event):
        pass

    @handles_event('my_other_event')
    def do_something_else(event):
        pass

Running tests
-------------
Just run `python manage.py test` to run tests against your current setup. Run `tox` to run tests for various versions of
Django. Currently, Django 1.6 through 1.9 on Python 2.7 are tested.
