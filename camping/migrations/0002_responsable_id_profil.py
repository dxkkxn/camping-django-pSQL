# Generated by Django 3.1.4 on 2020-12-14 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='id_profil',
            field=models.ForeignKey(db_column='id_profil', default=1, on_delete=django.db.models.deletion.CASCADE, to='camping.profil'),
            preserve_default=False,
        ),
    ]