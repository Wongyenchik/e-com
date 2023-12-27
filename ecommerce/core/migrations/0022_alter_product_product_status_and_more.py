# Generated by Django 4.2.7 on 2023-12-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0021_alter_product_product_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("disabled", "Disabled"),
                    ("published", "Published"),
                    ("in_review", "In Review"),
                    ("rejected", "Rejected"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="productreview",
            name="rating",
            field=models.IntegerField(
                choices=[
                    (1, "★☆☆☆☆"),
                    (2, "★★☆☆☆"),
                    (5, "★★★★★"),
                    (3, "★★★☆☆"),
                    (4, "★★★★☆"),
                ],
                default=None,
            ),
        ),
    ]
