# Generated by Django 5.1 on 2024-10-01 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0003_delete_extracurricularactivity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolprofile',
            old_name='school_name',
            new_name='school',
        ),
        migrations.RenameField(
            model_name='schoolsubject',
            old_name='schoolprofile_name',
            new_name='school',
        ),
    ]