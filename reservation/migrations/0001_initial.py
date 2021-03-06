# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 09:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reservation.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(validators=(reservation.validators.validate_working_hours, reservation.validators.validate_not_in_past, reservation.validators.validate_not_late, reservation.validators.validate_not_weekend))),
                ('end_date', models.DateTimeField(validators=(reservation.validators.validate_working_hours, reservation.validators.validate_not_in_past, reservation.validators.validate_not_late, reservation.validators.validate_not_weekend))),
                ('theme', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('answer', models.IntegerField(choices=[(0, 'Deny'), (1, 'Allow'), (2, 'Pending')], default=2)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
