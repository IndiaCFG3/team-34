# Generated by Django 2.2 on 2020-08-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200816_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]