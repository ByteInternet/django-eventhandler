===================
django-eventhandler
===================

.. image:: https://travis-ci.org/ByteInternet/django-eventhandler.svg?branch=master
   :target: https://travis-ci.org/ByteInternet/django-eventhandler

This is an event handler that handles messages from an AMQP server, installable as a Django application. Events are
JSON-encoded dicts that have a key called 'type'. The eventhandler calls functions that have bound themselves to an
event using a decorator.


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
Events that are received from AMQP should be JSON-encoded dicts. Each message should have a key named `type`, with `str`
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


**NB** Make sure that your handlers are in a place that's loaded/scanned on startup of Django,
 otherwise the decorators won't register the handlers. For instance, for a Django-application,
 `my_app/__init__.py` is scanned on startup (provided `my_app` is in `INSTALLED_APPS`). So if
 your handlers are in `my_app/events.py`, you could load them from there:

.. code-block:: python

    # my_app/__init__.py:

    # Load handlers for events, so django-eventhandlers picks 'em up
    import my_app.events  # NOQA (keep pyflakes happy)


Running tests
-------------
Just run `python manage.py test` to run tests against your current setup.


=====
About
=====
This software is brought to you by Byte, a webhosting provider based in Amsterdam, The Netherlands. We specialize in
fast and secure Magento hosting and scalable cluster hosting.

Check out our `Github page <https://github.com/ByteInternet>`_ for more open source software or `our site <https://www.byte.nl>`_
to learn about our products and technologies. Look interesting? Reach out about `joining the team <https://www.byte.nl/vacatures>`_.
Or just drop by for a cup of excellent coffee if you're in town!
