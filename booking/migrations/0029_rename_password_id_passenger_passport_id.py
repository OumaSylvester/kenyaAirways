# Generated by Django 4.2.3 on 2023-08-01 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0028_rename_flight_route_rename_flight_aeroplane_route_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="passenger",
            old_name="password_id",
            new_name="passport_id",
        ),
    ]