# Generated by Django 4.2.1 on 2023-07-23 07:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recurring_expenses", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recurringexpense",
            old_name="fee",
            new_name="amount",
        ),
    ]
