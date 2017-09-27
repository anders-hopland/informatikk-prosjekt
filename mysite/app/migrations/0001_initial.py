# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(max_length=250)),
                ('sjanger', models.CharField(max_length=250)),
                ('krav', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='extend_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Konsert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_tidspunkt', models.DateField()),
                ('a_navn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='rigging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ManyToManyField(to='app.extend_user')),
            ],
        ),
        migrations.CreateModel(
            name='Tilbud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pris', models.IntegerField()),
                ('ex_date', models.DateField()),
                ('a_navn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Konsert')),
            ],
        ),
        migrations.AddField(
            model_name='konsert',
            name='rigging',
            field=models.ManyToManyField(to='app.rigging'),
        ),
    ]