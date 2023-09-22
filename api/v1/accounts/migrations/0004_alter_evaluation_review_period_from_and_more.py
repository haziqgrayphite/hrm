# Generated by Django 4.2.4 on 2023-09-20 05:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='review_period_from',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 9, 20, 5, 14, 7, 294318, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='review_period_to',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 9, 20, 5, 14, 7, 294350, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
