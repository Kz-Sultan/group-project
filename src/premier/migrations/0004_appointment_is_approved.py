# Generated by Django 5.2.2 on 2025-07-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premier', '0003_contact_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
