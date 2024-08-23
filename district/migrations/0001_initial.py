# Generated by Django 5.0.6 on 2024-08-21 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.PositiveIntegerField(blank=True, default=2024, null=True)),
                ('term_1_start_date', models.DateField(blank=True, null=True)),
                ('term_1_end_date', models.DateField(blank=True, null=True)),
                ('term_2_start_date', models.DateField(blank=True, null=True)),
                ('term_2_end_date', models.DateField(blank=True, null=True)),
                ('term_3_start_date', models.DateField(blank=True, null=True)),
                ('term_3_end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='District_School_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_level', models.IntegerField(choices=[(8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')])),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='DistrictAdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('admin', models.CharField(blank=True, choices=[('admin1', 'admin1'), ('admin2', 'admin2'), ('admin3', 'admin3')], max_length=10, null=True)),
                ('district_admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='district_admin_profile', to=settings.AUTH_USER_MODEL)),
                ('district_schools', models.ManyToManyField(to='district.district_school_registration')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=200)),
                ('note', models.TextField()),
                ('academic_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to='district.academiccalendar')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolAdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('admin', models.CharField(blank=True, choices=[('admin1', 'admin1'), ('admin2', 'admin2'), ('admin3', 'admin3')], max_length=10, null=True)),
                ('assigned_school_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.district_school_registration')),
                ('school_admin', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolHeadProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('assigned_school_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='district.district_school_registration')),
                ('school_head', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='SchoolHead_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]