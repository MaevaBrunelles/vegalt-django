"""
WSGI config for vegalt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

import sys

path = '/Users/mbrunell/Documents/Dev/OC-Python/P8-Vegalt-Django/vegalt-django'  # use your own username here
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegalt.settings')

application = get_wsgi_application()
