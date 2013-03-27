# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth import logout

def site_logout(request):
    if request.user.is_authenticated():
        logout(request)
        return render_to_response('registration/logout.html',  {'request': request})
    return render_to_response('registration/logout.html',  {'request': request})


