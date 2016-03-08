#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command


settings.configure(
    INSTALLED_APPS=('eventhandler',),
    DATABASES=dict(
        default=dict(
            ENGINE='django.db.backends.sqlite3',
        )
    ),
)

if __name__ == "__main__":
    call_command('test', 'eventhandler')
