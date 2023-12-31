# Generated by Django 4.2.7 on 2023-12-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0031_vendor_rating12_alter_cartorder_product_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("shipped", "Shipped"),
                    ("processing", "Processing"),
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
                    ("in_review", "In Review"),
                    ("rejected", "Rejected"),
                    ("draft", "Draft"),
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
                    (3, "★★★☆☆"),
                    (2, "★★☆☆☆"),
                    (1, "★☆☆☆☆"),
                    (5, "★★★★★"),
                    (4, "★★★★☆"),
                ],
                default=None,
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="rating12",
            field=models.IntegerField(
                choices=[
                    (3, "★★★☆☆"),
                    (2, "★★☆☆☆"),
                    (1, "★☆☆☆☆"),
                    (5, "★★★★★"),
                    (4, "★★★★☆"),
                ],
                default=None,
            ),
        ),
    ]
