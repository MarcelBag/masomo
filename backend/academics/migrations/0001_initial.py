# Generated by Django 5.1.5 on 2025-05-31 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_current', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('room', models.CharField(blank=True, max_length=30)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classes', to='academics.academicyear')),
                ('main_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homerooms', to='teachers.teacher')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'academic_year')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=80)),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='academics.schoolclass')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subjects', to='teachers.teacher')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('code', 'school_class')},
            },
        ),
    ]
