"""
WSGI config for uploads project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# sys.path.append('/opt/python/current/app/')
# sys.path.append('/opt/python/current/app/uploads/wsgi.py')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uploads.settings")

application = get_wsgi_application()
