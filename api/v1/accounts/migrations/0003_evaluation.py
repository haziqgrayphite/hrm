# Generated by Django 4.2.4 on 2023-09-20 05:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.JSONField(default=dict)),
                ('review_period_from', models.DateField(blank=True, default=datetime.datetime(2023, 9, 20, 5, 2, 54, 460504, tzinfo=datetime.timezone.utc), null=True)),
                ('review_period_to', models.DateField(blank=True, default=datetime.datetime(2023, 9, 20, 5, 2, 54, 460532, tzinfo=datetime.timezone.utc), null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_completed', models.BooleanField(default=False)),
                ('overall_comments', models.CharField(blank=True, null=True)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='evaluations_by', to=settings.AUTH_USER_MODEL)),
                ('evaluatee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='evaluations_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]