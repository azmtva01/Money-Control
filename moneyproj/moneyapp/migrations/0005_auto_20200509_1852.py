# Generated by Django 3.0.6 on 2020-05-09 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyapp', '0004_auto_20200509_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget_choice',
            field=models.CharField(blank=True, choices=[('income', 'income'), ('expense', 'expense')], default='expense', max_length=7, verbose_name='Budget Choice'),
        ),
    ]
