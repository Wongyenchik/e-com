# Generated by Django 4.2.7 on 2023-12-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0040_alter_cartorder_product_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("processing", "Processing"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                ],
                default="processing",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("rejected", "Rejected"),
                    ("in_review", "In Review"),
                    ("published", "Published"),
                    ("disabled", "Disabled"),
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
                    (4, "★★★★☆"),
                    (3, "★★★☆☆"),
                    (1, "★☆☆☆☆"),
                    (2, "★★☆☆☆"),
                    (5, "★★★★★"),
                ],
                default=None,
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="avg_rating",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
