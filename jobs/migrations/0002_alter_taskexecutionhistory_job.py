# Generated by Django 4.2.10 on 2024-04-07 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskexecutionhistory",
            name="job",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="jobs.job"),
        ),
    ]
