from django.db import models

# Create your models here.

class Client(models.Model):
    num_client = models.AutoField(primary_key = True)
    nom_client = models.CharField(max_length = 30)
    prenom_client = models.CharField(max_length = 30)
    adresse = models.CharField(max_length = 50)
    telephone = models.IntegerField()
    date_de_naissance = models.DateField()#
    # Num_carte = models.AutoField()
    email = models.EmailField()
    password= models.CharField(max_length= 30)


class Test(models.Model):
    test = models.TextField()
