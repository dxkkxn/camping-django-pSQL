# Generated by Django 3.1.3 on 2020-12-02 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='client',
            name='age18ans',
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.CheckConstraint(check=models.Q(date_de_naissance__lte=datetime.date(2002, 12, 3)), name='age18ans'),
        ),
    ]
