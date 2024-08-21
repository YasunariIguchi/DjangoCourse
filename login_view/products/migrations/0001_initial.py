# Generated by Django 5.0.7 on 2024-08-21 05:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("create_at", models.DateTimeField()),
                ("update_at", models.DateTimeField()),
                ("name", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("type1", "Type 1"),
                            ("type2", "Type 2"),
                            ("type3", "Type 3"),
                            ("type4", "Type 4"),
                            ("type5", "Type 5"),
                            ("type6", "Type 6"),
                            ("type7", "Type 7"),
                            ("type8", "Type 8"),
                            ("type9", "Type 9"),
                            ("type10", "Type 10"),
                        ],
                        max_length=10,
                    ),
                ),
                ("price", models.PositiveIntegerField()),
                ("stock", models.PositiveIntegerField()),
                (
                    "producer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="Picture",
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
                ("create_at", models.DateTimeField()),
                ("update_at", models.DateTimeField()),
                ("picture", models.FileField(upload_to="picture")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "db_table": "pictures",
            },
        ),
    ]
