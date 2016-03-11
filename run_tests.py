#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
from django.core.management import call_command


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    django.setup()
    call_command('test')
