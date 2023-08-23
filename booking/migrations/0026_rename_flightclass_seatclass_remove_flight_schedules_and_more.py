# Generated by Django 4.2.3 on 2023-07-30 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0025_remove_schedule_aeroplane_time_aeroplane_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FlightClass",
            new_name="SeatClass",
        ),
        migrations.RemoveField(
            model_name="flight",
            name="schedules",
        ),
        migrations.AddField(
            model_name="aeroplane",
            name="flight",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="aeroplanes",
                to="booking.flight",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="schedule",
            name="flights",
            field=models.ManyToManyField(related_name="schedules", to="booking.flight"),
        ),
    ]