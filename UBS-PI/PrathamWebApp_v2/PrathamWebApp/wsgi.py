"""
WSGI config for PrathamWebApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
sys.path.insert(0, '/var/www/html/UBS-PI/PrathamWebApp_v2')
sys.path.insert(0,"/var/www/html/UBS-PI/UBS/lib/python3.6/site-packages")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PrathamWebApp.settings')

application = get_wsgi_application()
