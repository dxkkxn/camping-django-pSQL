# Generated by Django 3.1.3 on 2020-11-30 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camping', '0003_auto_20201130_2147'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='client',
            table='client',
        ),
        migrations.AlterModelTable(
            name='reservation',
            table='reservation',
        ),
    ]