#!/usr/bin/env python
import os
import sys
from ast import literal_eval

if __name__ == "__main__":
    with open(".env", "r") as ptr:
        for line in ptr:
            line = line.strip()
            if "#" != line[0]:
                var, val = line.split("=", 1)
                os.environ[var] = literal_eval(val)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paas.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
