# Generated by Django 4.0.4 on 2022-05-16 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0003_cycleslength_date_added_alter_cycleslength_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cycleslength',
            name='date_added',
        ),
    ]
