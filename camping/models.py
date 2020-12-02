from django.db import models
from .scripts import date_18_years_before
# Create your models here.
date = date_18_years_before()
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

    class Meta:
        db_table = "client"
        constraints = [
            models.CheckConstraint(check=(models.Q(telephone__gte = 100000000,
                                                    telephone__lt = 1000000000)),
            name='tel_digits'),

            models.CheckConstraint(check=(models.Q(date_de_naissance__lte = date)),
            name='age18ans'),
            models.UniqueConstraint(name = "email unique"  , fields = ["email"])
        ]

# and telephone <= 1000000000
class Responsable:
    email = models.EmailField()
    password= models.CharField(max_length= 30)
    num_client = models.ForeignKey(Client, on_delete = models.CASCADE)

    class Meta:
        db_table = "responsable"

class Reservation(models.Model):
    num_client = models.ForeignKey(Client, on_delete = models.CASCADE)
    num_reservation = models.AutoField(primary_key = True)
    acompte = models.IntegerField()
    date_reservation = models.DateField()
    debut_sejour = models.DateField()
    fin_sejour = models.DateField()

    class Meta:
        db_table = "reservation"

class ServicesProposes(models.Model):
    services_proposes = models.Charfield()
    prix_suplement    = models.IntegerField()

    class Meta:
        db_table = "services_proposes"

class ReservationServices(models.Model):
    num_reservation = models.ForeignKey(Reservation, on_delete = models.CASCADE)
    services_proposes = models.ForeignKey(ServicesProposes,
                                            on_delete = models.CASCADE)
    class Meta:
        db_table = "services_reservation"

class Fidelite:
    point_fidelite = models.IntegerField(primary_key = True)
    reduc_fidelite = models.IntegerField()
    num_client     = models.ForeignKey(Client, on_delete = models.CASCADE)
    class Meta:
        db_table = "fidelite"

class Sport:
    nom_sport = models.CharField(primary_key = True, max_length = 30)
    tarif_unite = models.DecimalField(max_digits = 10, decimal_places = 2)
    class Meta:
        db_table = "sport"
    
