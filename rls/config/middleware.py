from django.db import connection
from contextlib import contextmanager


@contextmanager
def tenant_context(tenant_id: int):
    """enter tenant context with tenant_id
    ::

        # without tenant RLS

        with tenant_context(tenant_id):
            # All commands here are ran under the `tenant_id` RLS

        # without tenant RLS
    """
    with connection.cursor() as cursor:
        cursor.execute(f'SET ROLE "{tenant_id}" ')
        yield
        cursor.execute(f'RESET ROLE')


# set db role for RLS control. see: https://scrapbox.io/shimizukawa/Django_PG_RLS
class RlsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = getattr(request.user, 'tenant_id', None)
        if tenant_id:
            with tenant_context(tenant_id):
                response = self.get_response(request)
        else:  # for administration of all tenants.
            response = self.get_response(request)
        return response