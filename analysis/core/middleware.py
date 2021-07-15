import jwt
from django.http import HttpResponseForbidden

from analysis.conf.yconfig import YConfig
from analysis.models import Chives


class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # only ajax request need auth
        if request.path != '/analysis/api/chives/signin' and (request.is_ajax() or request.path.startswith('/analysis/api/')):
            request.chives = None
            jwt_token = request.headers.get('authorization', None)
            print(jwt_token)
            if jwt_token:
                try:
                    payload = jwt.decode(jwt_token, YConfig.get('jwt:secret'),
                                         algorithms=YConfig.get('jwt:algorithm'))
                except (jwt.DecodeError, jwt.ExpiredSignatureError):
                    return HttpResponseForbidden()

                request.chives = Chives.objects.get(id=payload['chives_id'])
            else:
                return HttpResponseForbidden()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

