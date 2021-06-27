# Generated by Django 3.2 on 2021-04-22 17:56

from django.db import migrations
from django.conf import settings


def get_grant_sql():
    """GRANT用SQL"""
    # FIXME: このGRANTは新しいテーブルが追加される毎に実行が必要
    sql = f"""
        GRANT ALL ON ALL TABLES IN SCHEMA public TO {settings.RLS_ROLE_NAME};
        GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO {settings.RLS_ROLE_NAME};
    """
    return sql


def get_revoke_sql():
    """REVOKE用SQL"""
    sql = f"""
        REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM {settings.RLS_ROLE_NAME};
        REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {settings.RLS_ROLE_NAME};
    """
    return sql


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        # データ投入より先に必要なロールを作成
        migrations.RunSQL(
            f"CREATE ROLE {settings.RLS_ROLE_NAME};",
            reverse_sql=f"DROP ROLE {settings.RLS_ROLE_NAME};"
        ),
        # アプリからデータアクセスを許可する（django_session, django_admin_logは必須）
        migrations.RunSQL(get_grant_sql(), reverse_sql=get_revoke_sql())
    ]
