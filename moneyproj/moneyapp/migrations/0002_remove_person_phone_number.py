# Generated by Django 3.0.6 on 2020-05-07 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneyapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
    ]