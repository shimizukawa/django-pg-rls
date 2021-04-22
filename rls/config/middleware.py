from django.db import connection


# set db role for RLS control. see: https://scrapbox.io/shimizukawa/Django_PG_RLS
class RlsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = getattr(request.user, 'tenant_id', None)
        if tenant_id:
            with connection.cursor() as cursor:
                cursor.execute(f'SET ROLE "{tenant_id}" ')

        response = self.get_response(request)
        return response