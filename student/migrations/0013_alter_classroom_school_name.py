# Generated by Django 5.1 on 2024-09-19 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0003_delete_extracurricularactivity'),
        ('student', '0012_classroom_school_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='school_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customsettings.schoolprofile'),
        ),
    ]