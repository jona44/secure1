# Generated by Django 5.1 on 2024-09-17 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customsettings', '0002_extracurricularactivity'),
        ('student', '0008_extracurricularactivity_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExtraCurricularActivity',
        ),
    ]
