# Generated by Django 5.1.7 on 2025-03-20 07:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0003_meal_stock_alter_meal_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderTransaction",
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
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=64,
                        verbose_name="Amount Paid (Rs)",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("failed", "FAILED"),
                            ("completed", "COMPLETED"),
                            ("pending", "PENDING"),
                        ],
                        max_length=10,
                        verbose_name="Delivery Status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date created"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurant.meal",
                    ),
                ),
            ],
        ),
    ]
