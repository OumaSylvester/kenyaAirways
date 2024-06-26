# Generated by Django 4.2.3 on 2023-07-23 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0003_rename_schedule_flight_schedules"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="booking.flight",
            ),
        ),
    ]
