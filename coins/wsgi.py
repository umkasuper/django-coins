#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WSGI config for coins project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/maksimkolesnikov/Developer/python/coins-env/lib/python3.5/site-packages')

sys.path.append('/home/maksimkolesnikov/django-coins')

#paths = [
#    '/home/maksimkolesnikov/django-coins',
#]
#
#for path in paths:
#    if path not in sys.path:
#        sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coins.settings")


activate_env = os.path.expanduser("/home/maksimkolesnikov/Developer/python/coins-env/bin/activate_this.py")

exec(compile(open(activate_env, "rb").read(), activate_env, 'exec'), dict(__file__=activate_env))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
