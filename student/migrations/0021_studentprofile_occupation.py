# Generated by Django 5.0.6 on 2024-12-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_studentschoolhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
