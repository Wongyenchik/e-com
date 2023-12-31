# Generated by Django 4.2.7 on 2023-11-25 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_product_product_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="tags",
        ),
        migrations.AddField(
            model_name="product",
            name="vendor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.vendor",
            ),
        ),
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("process", "Processing"),
                    ("delivered", "Delivered"),
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
                    ("in_review", "In Review"),
                    ("rejected", "Rejected"),
                    ("disabled", "Disabled"),
                    ("published", "Published"),
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
                    (4, "★★★★☆"),
                    (2, "★★☆☆☆"),
                    (5, "★★★★★"),
                    (1, "★⭒☆☆☆"),
                    (3, "★★★☆☆"),
                ],
                default=None,
            ),
        ),
    ]
