# Generated by Django 4.2.1 on 2023-07-23 06:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("bank_accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecurringExpense",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("particulars", models.CharField(max_length=256)),
                ("currency", models.CharField(max_length=3)),
                ("period", models.IntegerField()),
                ("fee", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="bank_accounts.bankaccount",
                    ),
                ),
            ],
        ),
    ]
