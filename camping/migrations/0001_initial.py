# Generated by Django 3.1.3 on 2020-11-24 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('num_client', models.AutoField(primary_key=True, serialize=False)),
                ('nom_client', models.CharField(max_length=30)),
                ('prenom_client', models.CharField(max_length=30)),
                ('adresse', models.CharField(max_length=50)),
                ('telephone', models.IntegerField()),
                ('date_de_naissance', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.TextField()),
            ],
        ),
    ]