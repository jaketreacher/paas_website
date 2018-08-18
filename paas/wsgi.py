"""
WSGI config for paas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from ast import literal_eval


with open(".env", "r") as ptr:
    for line in ptr:
        line = line.strip()
        if "#" != line[0]:
            var, val = line.split("=", 1)
            os.environ[var] = literal_eval(val)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paas.settings")

application = get_wsgi_application()
