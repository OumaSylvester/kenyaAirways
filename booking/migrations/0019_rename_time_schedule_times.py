# Generated by Django 4.2.3 on 2023-07-28 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0018_remove_seat_price_flight_flight_class_flight_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="schedule",
            old_name="time",
            new_name="times",
        ),
    ]