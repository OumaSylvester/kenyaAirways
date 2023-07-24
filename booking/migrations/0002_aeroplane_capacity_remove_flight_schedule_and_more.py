# Generated by Django 4.2.3 on 2023-07-23 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aeroplane",
            name="capacity",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="flight",
            name="schedule",
        ),
        migrations.AlterField(
            model_name="schedule",
            name="aeroplane",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="schedules",
                to="booking.aeroplane",
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="schedule",
            field=models.ManyToManyField(to="booking.schedule"),
        ),
    ]
