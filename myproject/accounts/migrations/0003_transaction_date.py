# Generated by Django 5.1.7 on 2025-04-01 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_dailyrecord_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
