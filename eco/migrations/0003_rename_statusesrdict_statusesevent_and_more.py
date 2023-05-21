# Generated by Django 4.2 on 2023-04-27 18:36

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0002_sortpoints_photo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StatusesRDict',
            new_name='StatusesEvent',
        ),
        migrations.RenameModel(
            old_name='StatusesDict',
            new_name='StatusesReport',
        ),
        migrations.RenameField(
            model_name='statusesevent',
            old_name='status_id_r',
            new_name='status_id',
        ),
        migrations.RenameField(
            model_name='statusesreport',
            old_name='status_id',
            new_name='status_id_r',
        ),
        migrations.RemoveField(
            model_name='events',
            name='latitude_n',
        ),
        migrations.RemoveField(
            model_name='events',
            name='longitude_e',
        ),
        migrations.AlterField(
            model_name='districts',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='events',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='district_id',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='admarea_id', chained_model_field='admarea_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='eco.districts'),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='latitude_n',
            field=models.DecimalField(decimal_places=8, max_digits=10, max_length=9),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='longitude_e',
            field=models.DecimalField(decimal_places=8, max_digits=11, max_length=9),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='organization_inn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eco.organizations'),
        ),
        migrations.AlterField(
            model_name='natureobjects',
            name='transport_description',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='reports',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='routes',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='routes',
            name='end_e',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='routes',
            name='end_n',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='routes',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='routes',
            name='start_e',
            field=models.DecimalField(decimal_places=8, max_digits=11),
        ),
        migrations.AlterField(
            model_name='routes',
            name='start_n',
            field=models.DecimalField(decimal_places=8, max_digits=10),
        ),
        migrations.AlterField(
            model_name='routes',
            name='transport_description',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='district_id',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='admarea_id', chained_model_field='admarea_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='eco.districts'),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='latitude_n',
            field=models.DecimalField(decimal_places=8, max_digits=10, max_length=9),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='longitude_e',
            field=models.DecimalField(decimal_places=8, max_digits=11, max_length=9),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='organization_inn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.organizations'),
        ),
        migrations.AlterField(
            model_name='sortpoints',
            name='transport_description',
            field=models.TextField(max_length=512),
        ),
    ]
