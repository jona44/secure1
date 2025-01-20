# Generated by Django 5.0.6 on 2024-12-14 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '0005_remove_holiday_academic_calendar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='district_school_registration',
            name='district',
            field=models.ForeignKey(blank=True, choices=[('Khayelitsha', 'Khayelitsha'), ('Kraaifontain', 'BKraaifontain'), ('Dunoon', 'Dunoon'), ('Mitchelles Plain', 'Mitchelles Plain'), ('Somerset West', 'Somerset West')], null=True, on_delete=django.db.models.deletion.CASCADE, to='district.district'),
        ),
    ]