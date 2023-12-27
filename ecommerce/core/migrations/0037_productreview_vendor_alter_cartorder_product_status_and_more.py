# Generated by Django 4.2.7 on 2023-12-26 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_remove_vendor_rating_vendor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productreview",
            name="vendor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vendor1",
                to="core.vendor",
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
                    ("draft", "Draft"),
                    ("disabled", "Disabled"),
                    ("rejected", "Rejected"),
                    ("published", "Published"),
                    ("in_review", "In Review"),
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
                    (4, "★★★★☆"),
                    (2, "★★☆☆☆"),
                    (1, "★☆☆☆☆"),
                    (5, "★★★★★"),
                ],
                default=None,
            ),
        ),
    ]