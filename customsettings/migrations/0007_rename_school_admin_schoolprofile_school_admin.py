# Generated by Django 5.0.6 on 2024-12-23 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0006_schoolprofile_school_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolprofile',
            old_name='School_admin',
            new_name='school_admin',
        ),
    ]
