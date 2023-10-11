# Generated by Django 4.2.4 on 2023-10-11 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_until', models.DateTimeField()),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('expiry_days', models.IntegerField(blank=True, default=7, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_expired', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_expirable', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('evaluatees', models.ManyToManyField(related_name='assigned_evaluation_evaluatees', to=settings.AUTH_USER_MODEL)),
                ('evaluators', models.ManyToManyField(related_name='assigned_evaluation_evaluators', to=settings.AUTH_USER_MODEL)),
                ('parameters', models.ManyToManyField(related_name='assigned_parameter', to='evaluation.parameter')),
            ],
        ),
        migrations.CreateModel(
            name='OverallEvaluationScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_evaluated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overall_evaluation_scores', to='evaluation.evaluation')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overall_evaluation_scores', to='evaluation.parameter')),
                ('parameter_rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overall_evaluation_scores', to='evaluation.parameterrating')),
            ],
        ),
        migrations.RemoveField(
            model_name='evaluationscore',
            name='evaluation',
        ),
        migrations.RemoveField(
            model_name='evaluationscore',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='evaluationscore',
            name='parameter_rating',
        ),
        migrations.DeleteModel(
            name='BaseEvaluation',
        ),
        migrations.DeleteModel(
            name='EvaluationScore',
        ),
    ]