# Generated by Django 4.2.3 on 2023-07-24 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0007_rename_sits_sit_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Sit",
            new_name="Seat",
        ),
        migrations.RenameIndex(
            model_name="seat",
            new_name="booking_sea_sit_no_424782_idx",
            old_name="booking_sit_sit_no_6413b5_idx",
        ),
    ]
