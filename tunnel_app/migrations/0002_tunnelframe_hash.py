# Generated by Django 3.2.4 on 2021-07-27 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunnel_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tunnelframe',
            name='hash',
            field=models.SlugField(max_length=8, null=True),
        ),
    ]
