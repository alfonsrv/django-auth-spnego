import asyncio
from functools import wraps

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def login_required_spnego(view_func):
    """ Decorator for views that checks if the user is currently logged in and
    if they aren't tries to authenticate them auto-magically via SPNEGO.
    This allows accessing an endpoint via SSO without having to be redirected
    to a dedicated login-view first, making resource-access more seamless. """

    def authenticate_spnego(request):
        response = HttpResponse()
        response['WWW-Authenticate'] = 'Negotiate'
        response.status_code = 401

        if 'Negotiate' in request.META.get('HTTP_AUTHORIZATION', ''):
            user = authenticate(
                request, spnego=request.META['HTTP_AUTHORIZATION'].split()[1]
            )
            if not user:
                return response

            if gssresponse := user.gssresponse:
                response['WWW-Authenticate'] = 'Negotiate {}'.format(gssresponse)
            else:
                del(response['WWW-Authenticate'])
            response.status_code = 200
            login(request, user)
        return response

    if asyncio.iscoroutinefunction(view_func):
        async def _view_wrapper(request, *args, **kwargs):
            auser = await request.auser()
            authenticated = auser.is_authenticated

            if not authenticated:
                auth_response = await sync_to_async(authenticate_spnego)(request)
                if auth_response.status_code != 200:
                    return auth_response

            response = await view_func(request, *args, **kwargs)
            return response
    else:
        def _view_wrapper(request, *args, **kwargs):
            authenticated = request.user.is_authenticated
            if not authenticated:
                auth_response = authenticate_spnego(request)
                if auth_response.status_code != 200:
                    return auth_response

            response = view_func(request, *args, **kwargs)
            return response

    return wraps(view_func)(_view_wrapper)
