# Generated by Django 5.1.4 on 2025-01-02 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0010_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="title",
            name="director",
            field=models.ForeignKey(
                blank=True,
                db_column="director_id",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="movie.direct",
            ),
        ),
    ]
