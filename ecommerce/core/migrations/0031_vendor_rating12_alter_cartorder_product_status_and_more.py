# Generated by Django 4.2.7 on 2023-12-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0030_remove_vendor_avg_rating_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="rating12",
            field=models.IntegerField(
                choices=[
                    (3, "★★★☆☆"),
                    (5, "★★★★★"),
                    (2, "★★☆☆☆"),
                    (1, "★☆☆☆☆"),
                    (4, "★★★★☆"),
                ],
                default=None,
            ),
        ),
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("delivered", "Delivered"),
                    ("processing", "Processing"),
                    ("shipped", "Shipped"),
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
                    ("published", "Published"),
                    ("in_review", "In Review"),
                    ("disabled", "Disabled"),
                    ("rejected", "Rejected"),
                    ("draft", "Draft"),
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
                    (5, "★★★★★"),
                    (2, "★★☆☆☆"),
                    (1, "★☆☆☆☆"),
                    (4, "★★★★☆"),
                ],
                default=None,
            ),
        ),
    ]