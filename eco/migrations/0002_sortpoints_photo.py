# Generated by Django 4.2 on 2023-04-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sortpoints',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]