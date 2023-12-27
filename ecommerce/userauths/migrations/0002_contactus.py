# Generated by Django 4.2.7 on 2023-12-07 01:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauths", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=200)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
            ],
        ),
    ]
