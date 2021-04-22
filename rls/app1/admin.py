from django.contrib import admin
from django.db.models.signals import post_save
from django.db import connection

from . import models


admin.site.register(models.Tenant)
admin.site.register(models.TenantUser)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'tel', 'email', 'tenant')
    list_display_links = ('id', 'name')


# create db role for RLS control. see: https://scrapbox.io/shimizukawa/Django_PG_RLS
def on_create_tenant(sender, instance, created, **kwargs):
    # FIXME: 削除時にはROLEも削除しておきたい（残っててもよい）
    if created:
        tenant_id = instance.id
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE ROLE "{tenant_id}"')
            cursor.execute(f'GRANT tenantuser TO "{tenant_id}"')


post_save.connect(on_create_tenant, sender=models.Tenant)
