# Generated by Django 3.2.4 on 2021-08-16 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunnel_app', '0014_auto_20210808_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='tunnelframe',
            name='column_depth_for_analysis',
            field=models.FloatField(choices=[(1, '1000mm'), (2, 'Column Width')], default=1),
        ),
    ]