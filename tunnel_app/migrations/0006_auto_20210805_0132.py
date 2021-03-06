# Generated by Django 3.2.4 on 2021-08-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunnel_app', '0005_auto_20210804_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaddefinition',
            name='force_end_depth',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AlterField(
            model_name='loaddefinition',
            name='force_start_depth',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
    ]
