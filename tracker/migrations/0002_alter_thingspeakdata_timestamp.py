# Generated by Django 4.2.2 on 2023-08-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thingspeakdata',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]