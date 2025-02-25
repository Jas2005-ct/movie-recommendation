# Generated by Django 5.1.4 on 2024-12-29 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0006_comedian"),
    ]

    operations = [
        migrations.CreateModel(
            name="music",
            fields=[
                ("music_id", models.AutoField(primary_key=True, serialize=False)),
                ("music", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField()),
                ("debut_movie", models.TextField()),
                ("debut_year", models.IntegerField()),
                ("img", models.ImageField(upload_to="pics")),
            ],
        ),
    ]
