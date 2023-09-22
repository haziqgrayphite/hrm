# Generated by Django 4.2.4 on 2023-09-21 12:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_evaluation_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='review_period_from',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 9, 21, 12, 45, 32, 975391, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='review_period_to',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 9, 21, 12, 45, 32, 975420, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
