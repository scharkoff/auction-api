from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            csrf_cookie = request.META.get('CSRF_COOKIE')
            if not csrf_cookie:
                csrf_token = request.COOKIES.get('csrftoken')
                if csrf_token:
                    request.META['HTTP_X_CSRFTOKEN'] = csrf_token
            else:
                request.META['HTTP_X_CSRFTOKEN'] = csrf_cookie

        return super().process_view(request, callback, callback_args, callback_kwargs)
