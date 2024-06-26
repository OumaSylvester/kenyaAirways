# Generated by Django 4.2.3 on 2023-07-29 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0021_alter_seat_seat_no"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="aeroplane",
            options={"verbose_name_plural": "Aeroplanes"},
        ),
        migrations.AlterModelOptions(
            name="time",
            options={"ordering": ["dep_time"]},
        ),
        migrations.RenameField(
            model_name="flight",
            old_name="price",
            new_name="price_A",
        ),
        migrations.RemoveField(
            model_name="flight",
            name="flight_class",
        ),
        migrations.AddField(
            model_name="booking",
            name="schedule",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="booking.schedule",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="booking",
            name="time",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="booking.time",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="flight",
            name="price_B",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="flight",
            name="price_C",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="seat",
            unique_together={("seat_no", "aeroplane")},
        ),
        migrations.AddIndex(
            model_name="time",
            index=models.Index(
                fields=["dep_time", "arrival_time"],
                name="booking_tim_dep_tim_2be7ed_idx",
            ),
        ),
    ]
