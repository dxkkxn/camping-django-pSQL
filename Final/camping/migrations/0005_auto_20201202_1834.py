# Generated by Django 3.1.3 on 2020-12-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camping', '0004_emplacement'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalleDeJeux',
            fields=[
                ('ref_jeu', models.AutoField(primary_key=True, serialize=False)),
                ('nom_jeu', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'salle_de_jeux',
            },
        ),
        migrations.AlterField(
            model_name='emplacement',
            name='num_empl',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
