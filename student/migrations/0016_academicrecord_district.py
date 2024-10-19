# Generated by Django 5.1 on 2024-10-01 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0003_delete_extracurricularactivity'),
        ('student', '0015_alter_studentprofile_school_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicrecord',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='customsettings.schoolprofile'),
        ),
    ]
