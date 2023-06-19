# Generated by Django 4.1.4 on 2023-06-19 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("eco", "0009_alter_natureobjects_schedule_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="photo",
            field=models.ImageField(blank=True, default="", upload_to="user/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="events",
            name="photo",
            field=models.ImageField(blank=True, default="", upload_to="events/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="events",
            name="status_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events",
                to="eco.statusesevent",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="natureobjects",
            name="photo",
            field=models.ImageField(
                blank=True, default="", upload_to="nature_objects/"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="reports",
            name="photo",
            field=models.ImageField(blank=True, default="", upload_to="reports/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="routes",
            name="photo",
            field=models.ImageField(blank=True, default="", upload_to="routes/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sortpoints",
            name="photo",
            field=models.ImageField(blank=True, default="", upload_to="sort_points/"),
            preserve_default=False,
        ),
    ]
