from django.contrib import admin
from django.db.models.signals import post_save, pre_delete
from django.db import connection
from django.conf import settings

from . import models


admin.site.register(models.Tenant)
admin.site.register(models.TenantUser)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'tel', 'email', 'tenant')
    list_display_links = ('id', 'name')


# create db role for RLS control. see: https://scrapbox.io/shimizukawa/Django_PG_RLS
def on_create_tenant(sender, instance, created, **kwargs):
    if created:
        tenant_id = instance.tenant_id
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE ROLE "{tenant_id}"')
            cursor.execute(f'GRANT {settings.RLS_ROLE_NAME} TO "{tenant_id}"')


post_save.connect(on_create_tenant, sender=models.Tenant)


def on_delete_tenant(sender, instance, using, **kwargs):
    """削除時にはROLEも削除しておく"""
    tenant_id = instance.tenant_id
    with connection.cursor() as cursor:
        cursor.execute(f'REVOKE {settings.RLS_ROLE_NAME} FROM "{tenant_id}"')
        cursor.execute(f'DROP ROLE "{tenant_id}"')


pre_delete.connect(on_delete_tenant, sender=models.Tenant)
