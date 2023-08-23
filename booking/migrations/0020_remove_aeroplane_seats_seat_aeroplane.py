# Generated by Django 4.2.3 on 2023-07-28 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0019_rename_time_schedule_times"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aeroplane",
            name="seats",
        ),
        migrations.AddField(
            model_name="seat",
            name="aeroplane",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seats",
                to="booking.aeroplane",
            ),
            preserve_default=False,
        ),
    ]