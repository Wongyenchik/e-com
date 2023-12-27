# Generated by Django 4.2.7 on 2023-11-25 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_cartorder_product_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("process", "Processing"),
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
                    ("disabled", "Disabled"),
                    ("draft", "Draft"),
                    ("in_review", "In Review"),
                    ("published", "Published"),
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
                    (5, "★★★★★"),
                    (2, "★★☆☆☆"),
                    (1, "★⭒☆☆☆"),
                    (4, "★★★★☆"),
                    (3, "★★★☆☆"),
                ],
                default=None,
            ),
        ),
    ]
