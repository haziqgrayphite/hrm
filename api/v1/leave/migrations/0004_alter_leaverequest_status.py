# Generated by Django 4.2.4 on 2023-10-27 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_alter_leaverequest_leaves_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'PENDING'), ('Approved', 'APPROVED'), ('Rejected', 'REJECTED'), ('Ambiguous', 'AMBIGUOUS')], default='Pending', max_length=20),
        ),
    ]
