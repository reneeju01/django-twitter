# Generated by Django 3.1.3 on 2022-01-22 22:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ('user', '-created_at')},
        ),
        migrations.AlterIndexTogether(
            name='tweet',
            index_together={('user', 'created_at')},
        ),
    ]
